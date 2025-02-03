import logging
from time import sleep
from typing import Literal

import groq
from groq import Groq
from mistralai import Mistral
from openai import BadRequestError, OpenAI, RateLimitError
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

logger = logging.getLogger(__name__)

class MaxContextError(Exception):
    """Exception to signal that the context is too large for the model."""
    def __init__(self, message: str):
        self.message = message

class Message:
    """Base class for tinysmith LLMAdapter messages.
    Subclasses are used to define the role of the message in the conversation.
    """
    content: str

    def __str__(self):
        return self.content
    def __repr__(self):
        return self.content

class SystemMessage(Message):
    role: Literal['system']
    content: str
    def __init__(self, content: str):
        self.role = 'system'
        self.content = content

class AssistantMessage(Message):
    role: Literal['assistant']
    content: str
    def __init__(self, content: str):
        self.role = 'assistant'
        self.content = content

class UserMessage(Message):
    role: Literal['user']
    content: str
    def __init__(self, content: str):
        self.role = 'user'
        self.content = content


# TODO: Remove token usage from the API.
#       This should be a private field that can be accessed through an API.
class LLMAdapter:
    """Base class for LLM adapters.
    
    This must be subclassed to create a new LLM adapter. Implement the `generate` method to 
    convert tinysmith Message objects into an underlying LLM response string.
    """
    def __init__(self,
                 model: str,
                 temperature: float,
                 top_p: float,
                 token_usage: dict,
                 api_key: None|str = None,
                 max_tokens: None|int = None):
        """Initialize the LLM adapter. This method must implement the API client initialization."""
        raise NotImplementedError

    def generate(self, messages: list[Message]) -> str:
        """Generate an LLM response from a list of tinysmith Message objects.
        
        This can use an API, or theoretically also direct invocation of a local model.
        """
        raise NotImplementedError



class MistralJSONAPIAdapter(LLMAdapter):
    """Use a Mistral-API compatible LLM server, using the JSON flag."""
    def __init__(self, model: str, temperature: float, top_p: float, api_key: None|str = None, max_tokens: None|int = None):
        # TODO: this might be broken
        assert api_key is not None, "Mistral API key must be provided."
        self.client = MistralClient(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens


    def generate(self, messages: list[Message]) -> str | None:
        system_prompt = None
        chat_completions = []
        for i, message in enumerate(messages):
            if isinstance(message, UserMessage):
                if system_prompt:
                    message_one = f"System: {system_prompt}\n\nUser: {message.content}"
                    chat_completions.append(ChatMessage(content=message_one, role='user'))
                    system_prompt = None
                    continue
                chat_completions.append(ChatMessage(content=message.content, role='user'))
            elif isinstance(message, AssistantMessage):
                chat_completions.append(ChatMessage(content=message.content, role='assistant'))
            elif isinstance(message, SystemMessage):
                if i != 0:
                    raise ValueError("System message must be the first message.")
                system_prompt = message.content

        for _ in range(3):
            try:
                response = self.client.chat(model=self.model, 
                                        messages=chat_completions,
                                        max_tokens=self.max_tokens,
                                        response_format={"type": "json_object"},
                                        temperature=self.temperature,
                                        top_p=self.top_p).choices[0].message.content
                if isinstance(response, list):
                    logger.warning(f"Mistral API returned a list of responses [{response}]. " \
                            + "Returning the first one.")
                    return response[0]
                return response 
            except MistralException as e:
                logger.warning(f"Failed to generate LLM response for: {e}")
                sleep(1)
                continue
        raise OverflowError("Too many errors encountered.")
         


class MistralAPIAdapter(LLMAdapter):
    """Use a Mistral-API compatible LLM server."""
    def __init__(self, model: str, temperature: float, top_p: float, token_usage: dict, api_key: None|str = None, max_tokens: None|int = None):
        assert api_key is not None, "Mistral API key must be provided."
        self.client = Mistral(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.usage = token_usage


    def generate(self, messages: list[Message]) -> str | None:
        system_prompt = None
        chat_completions = []
        for i, message in enumerate(messages):
            if isinstance(message, UserMessage):
                if system_prompt:
                    message_one = f"System:\n{system_prompt}\n\nUser:\n{message.content}"
                    chat_completions.append({'content': message_one, 'role': 'user'})
                    system_prompt = None
                    continue
                chat_completions.append({'content': message.content, 'role': 'user'})
            elif isinstance(message, AssistantMessage):
                chat_completions.append({'content': message.content, 'role': 'assistant'})
            elif isinstance(message, SystemMessage):
                if i != 0:
                    raise ValueError("System message must be the first message.")
                system_prompt = message.content

        for _ in range(3):
            api_response = self.client.chat.complete(model=self.model,
                                    messages=chat_completions,
                                    max_tokens=self.max_tokens,
                                    temperature=self.temperature,
                                    top_p=self.top_p)

            # Log usage
            self.usage['prompt_tokens'] = self.usage.get('prompt_tokens', 0) \
                    + api_response.usage.prompt_tokens
            self.usage['total_tokens'] = self.usage.get('total_tokens', 0) \
                + api_response.usage.total_tokens
            if api_response.usage.completion_tokens:
                self.usage['completion_tokens'] = self.usage.get('completion_tokens', 0) \
                        + api_response.usage.completion_tokens

            response = api_response.choices[0].message.content
            if isinstance(response, list):
                logger.warning(f"Mistral API returned a list of responses [{response}]. " \
                        + "Returning the first one.")
                return response[0]
            return response 
            # TODO: The old API provided MistralException. Figure out the exception that is thrown 
            #       here, when max context is reached.
            #except MistralException as e:
            #    if e.message and "too large for model" in e.message:
            #        raise MaxContextError("Max context error.")

            #    logger.warning(f"Failed to generate LLM response for: {e}")
            #    sleep(1)
            #    continue
        raise OverflowError("Too many errors encountered.")



class OpenAiAPIAdapter(LLMAdapter):
    """Use the official OpenAI API."""
    def __init__(self, model: str, 
                 temperature: float,
                 top_p: float,
                 token_usage: dict,
                 api_key: None|str = None,
                 max_tokens: None|int = None):
        assert api_key is not None, "OpenAI API key must be provided."
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.usage = token_usage

    def generate(self, messages: list[Message]) -> str | None:
        chat_completions = []
        for message in messages:
            if isinstance(message, UserMessage):
                chat_completions.append(ChatCompletionUserMessageParam(content=message.content, role='user'))
            elif isinstance(message, AssistantMessage):
                chat_completions.append(ChatCompletionAssistantMessageParam(content=message.content, role='assistant'))
            elif isinstance(message, SystemMessage):
                chat_completions.append(ChatCompletionSystemMessageParam(content=message.content, role='system'))
        for _ in range(3):
            try:
                api_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=chat_completions,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p
                    )
                response = api_response.choices[0].message.content
                
                if api_response.usage:
                    self.usage['prompt_tokens'] = self.usage.get('prompt_tokens', 0) \
                            + api_response.usage.prompt_tokens
                    self.usage['total_tokens'] = self.usage.get('total_tokens', 0) \
                            + api_response.usage.total_tokens
                    self.usage['completion_tokens'] = self.usage.get('completion_tokens', 0) \
                            + api_response.usage.completion_tokens

                return response 
            except RateLimitError as e:
                logger.warning(f"Rate Limit reached. Sleeping 60. Error: {e}")
                sleep(60)
                continue
            except BadRequestError as e:
                raise MaxContextError("Max context error. Error: {e}")
        raise OverflowError("Too many errors encountered.")



#class CustomAPIAdapter(LLMAdapter):
#    """Use an OpenAI-API compatible LLM server."""
#    def __init__(self, model: str, base_url: str, temperature: float, top_p: float, token_usage: dict, api_key: None|str = None, max_tokens: None|int = None):
#        self.client = OpenAI(base_url=base_url, api_key=api_key)
#        self.model = model
#        self.temperature = temperature
#        self.top_p = top_p
#        self.max_tokens = max_tokens
#        self.usage = token_usage
#
#    def generate(self, messages: list[Message]) -> str | None:
#        chat_completions = []
#        for message in messages:
#            if isinstance(message, UserMessage):
#                chat_completions.append(ChatCompletionUserMessageParam(content=message.content, role='user'))
#            elif isinstance(message, AssistantMessage):
#                chat_completions.append(ChatCompletionAssistantMessageParam(content=message.content, role='assistant'))
#            elif isinstance(message, SystemMessage):
#                chat_completions.append(ChatCompletionSystemMessageParam(content=message.content, role='system'))
#        for _ in range(3):
#            try:
#                api_response = self.client.chat.completions.create(
#                    model=self.model,
#                    messages=chat_completions,
#                    max_tokens=self.max_tokens,
#                    temperature=self.temperature,
#                    top_p=self.top_p
#                    )
#                response = api_response.choices[0].message.content
#                
#                if api_response.usage:
#                    self.usage['prompt_tokens'] = self.usage.get('prompt_tokens', 0) \
#                            + api_response.usage.prompt_tokens
#                    self.usage['total_tokens'] = self.usage.get('total_tokens', 0) \
#                            + api_response.usage.total_tokens
#                    self.usage['completion_tokens'] = self.usage.get('completion_tokens', 0) \
#                            + api_response.usage.completion_tokens
#
#                return response 
#            except RateLimitError as e:
#                logger.warning(f"Rate Limit reached. Sleeping 60. Error: {e}")
#                sleep(60)
#                continue
#            except BadRequestError as e:
#                raise MaxContextError("Max context error. Error: {e}")
#        raise OverflowError("Too many errors encountered.")



class HumanInputAdapter(LLMAdapter):
    """Use human input to emulate an LLM response. This can be used for debugging."""
    def __init__(self):
        pass

    def generate(self, messages: list[Message]) -> str | None:
        return input("> ")



class GroqAPIAdapter(LLMAdapter):
    """Use the groq API."""
    def __init__(self, model: str, temperature: float, top_p: float, token_usage: dict, api_key: None|str = None, max_tokens: None|int = None):
        assert api_key is not None, "Groq API key must be provided."
        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.usage = token_usage

    def generate(self, messages: list[Message]) -> str | None:
        chat_completions = []
        for message in messages:
            if isinstance(message, UserMessage):
                chat_completions.append(ChatCompletionUserMessageParam(content=message.content, role='user'))
            elif isinstance(message, AssistantMessage):
                chat_completions.append(ChatCompletionAssistantMessageParam(content=message.content, role='assistant'))
            elif isinstance(message, SystemMessage):
                chat_completions.append(ChatCompletionSystemMessageParam(content=message.content, role='system'))
        for _ in range(3):
            try:
                api_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=chat_completions,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p
                    )
                response = api_response.choices[0].message.content
                
                if api_response.usage:
                    self.usage['prompt_tokens'] = self.usage.get('prompt_tokens', 0) \
                            + api_response.usage.prompt_tokens
                    self.usage['total_tokens'] = self.usage.get('total_tokens', 0) \
                            + api_response.usage.total_tokens
                    self.usage['completion_tokens'] = self.usage.get('completion_tokens', 0) \
                            + api_response.usage.completion_tokens

                return response 
            except groq.RateLimitError as e:
                logger.warning(f"Rate Limit reached. Sleeping 60. Error: {e}")
                sleep(60)
                continue
            except groq.BadRequestError as e:
                raise MaxContextError("Max context error. Error: {e}")
        raise OverflowError("Too many errors encountered.")


# ============= Custom Adapter Copy


class CustomAPIAdapter(LLMAdapter):
    """Use the official OpenAI API."""
    def __init__(self, 
                 base_url: str,
                 model: str, 
                 temperature: float,
                 top_p: float,
                 token_usage: dict,
                 api_key: None|str = None,
                 max_tokens: None|int = None):
        assert api_key is not None, "OpenAI API key must be provided."
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.usage = token_usage

    def generate(self, messages: list[Message]) -> str | None:
        chat_completions = []
        for message in messages:
            if isinstance(message, UserMessage):
                chat_completions.append(ChatCompletionUserMessageParam(content=message.content, role='user'))
            elif isinstance(message, AssistantMessage):
                chat_completions.append(ChatCompletionAssistantMessageParam(content=message.content, role='assistant'))
            elif isinstance(message, SystemMessage):
                chat_completions.append(ChatCompletionSystemMessageParam(content=message.content, role='system'))
        for _ in range(3):
            try:
                api_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=chat_completions,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p
                    )
                response = api_response.choices[0].message.content
                
                if api_response.usage:
                    self.usage['prompt_tokens'] = self.usage.get('prompt_tokens', 0) \
                            + api_response.usage.prompt_tokens
                    self.usage['total_tokens'] = self.usage.get('total_tokens', 0) \
                            + api_response.usage.total_tokens
                    self.usage['completion_tokens'] = self.usage.get('completion_tokens', 0) \
                            + api_response.usage.completion_tokens

                return response 
            except RateLimitError as e:
                logger.warning(f"Rate Limit reached. Sleeping 60. Error: {e}")
                sleep(60)
                continue
            except BadRequestError as e:
                raise MaxContextError("Max context error. Error: {e}")
        raise OverflowError("Too many errors encountered.")

