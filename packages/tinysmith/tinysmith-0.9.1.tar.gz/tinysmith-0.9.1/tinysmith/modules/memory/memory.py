"""Memory Modules. Provide a way to store and retrieve information from the conversation history.

## Usage
state.get("memory_module") 
    returns -> {"memory": str}
"""
from collections import deque
import logging
import os

from tinysmith.llm.adapters import LLMAdapter, Message, SystemMessage, UserMessage
from tinysmith.modules.modules import Module
from tinysmith.modules.rag.utils import EmbeddedDocs
from tinysmith.orchestrator.state import State

logger = logging.getLogger(__name__)


_summary_system_prompt = """
You are the memory of an agent. You act as a summarizer to memorize all important facts. In addition to your current memory below, you receive a fact from the user.

### CURRENT MEMORY SUMMARY >>>>>
{memory}
<<<<< END CURRENT MEMORY SUMMARY

Always reply with a text summarizing your current memory including any new information.
- you *must* consider your current memory when replying
- you *must* evaluate if there is new information to add to your memory
- you *must not* repeat the same information in your memory
- you *must not* add 'CURRENT MEMORY SUMMARY' tags or other markers to your reply
- you *must not* mention yourself or your role
"""

_summary_user_prompt = """
> {response}
< {obs}
"""
class ReflectionLongTermMemory(Module):
    """Implementing long-term memory for reflections. This module is an adaption of the
    LongTermSummary Module and is used to store reflections in a long-term memory.

    Instead of executor responses it summarizes the reflector output from the global state.
    """
    def __init__(self, name: str, llm_adapter: LLMAdapter, storage_path: str, idx: int):
        """
        Args:
            name (str): Name of the memory module.
            llm_adapter (LLMAdapter): The LLM adapter to use for summarization.
        """
        self.name = name
        self.llm_adapter = llm_adapter
        self.summary = ""

        self.storage_path = storage_path
        self.idx = idx

        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

        self.init_memory = False
        file_path = os.path.join(storage_path, f"reflection_longterm_{idx}.mem")
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                self.summary = f.read()
                logger.debug(f"Memory loaded from {file_path}: {self.summary}")
                self.init_memory = True


    def preprocessing(self, obs: str, state: State) -> None:
        # make sure to initiate loaded reflections into memory
        if self.init_memory:
            memory_state = {"memory": self.summary}
            state.set(self.name, memory_state)
            self.init_memory = False
            return

        reflector_state = state.get("reflector")
        reflection = reflector_state.get("reflection") if reflector_state else None

        if not reflection:
            logger.debug("Skipping summary memory. No reflection.")
            return

        system_prompt = SystemMessage(_summary_system_prompt.format(memory=self.summary))
        user_prompt = UserMessage(_summary_user_prompt.format(response="Reflection:", obs=reflection))

        self.summary = self.llm_adapter.generate([system_prompt, user_prompt])
        
        memory_state = {"memory": self.summary}
        state.set(self.name, memory_state)
        logger.debug(f"Memory [{self.name}] updated: {self.summary}")

        file_path = os.path.join(self.storage_path, f"reflection_longterm_{self.idx}.mem")
        with open(file_path, "w") as f:
            f.write(self.summary)
            logger.debug(f"Memory saved to {file_path}")
        
        # Reset the reflection state
        reflector_state = {"reflection": None}
        state.set("reflector", reflector_state)


    def postprocessing(self, response: str, state: State) -> None:
        pass


    def reset(self):
        pass



class SummaryMemory(Module):
    """Implementing summary memory as described in by Wang et al.:
    'Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models'
    """
    def __init__(self, name: str, llm_adapter: LLMAdapter):
        """
        Args:
            name (str): Name of the memory module.
            llm_adapter (LLMAdapter): The LLM adapter to use for summarization.
        """
        self.llm_adapter = llm_adapter
        self.name = name
        self.summary = ""

    def preprocessing(self, obs: str, state: State) -> None:
        if obs is None:
            return
        response = state.get_response()
        system_prompt = SystemMessage(_summary_system_prompt.format(memory=self.summary))
        user_prompt = UserMessage(_summary_user_prompt.format(response=response, obs=obs))

        self.summary = self.llm_adapter.generate([system_prompt, user_prompt])
        
        memory_state = {"memory": self.summary}
        state.set(self.name, memory_state)
        logger.info(f"Memory updated: {self.summary}")

    def postprocessing(self, response: str, state: State) -> None:
        pass


    def reset(self):
        self.summary = ""




_rag_query_system_prompt = """You are the memory of an agent. You act as a retrieval assistant for the long-term memory system. 

Given an observation, you must generate queries to retrieve the most relevant information from the memory.

- You *must* consider the observation when generating the query.
- You *must* generate one query per line.
- You *must* prepend 'Query:' to each query line.

EXAMPLES >>>>>
Observation: "How is your wife doing, Jerry?"
Query: "Is my name Jerry?
Query: "What is the status of my relationship?"
Query: "How is my wife?"
---
Observation: "I am late because of the construction site near your house."
Query: "Is there a construction site near my house?"
Query: "Does the construction site usually affect traffic?"
---
Observation: "cat .flag.txt | base64 -d" "base64: invalid input"
Query: "What are the contents of the flag.txt file?"
Query: "Are there other relevant files in the directory?"
<<<<< END EXAMPLES
"""
class RAGMemory(Module):
    # TODO: test this memory module in a strategy
    def __init__(self, name: str, embedding_model: str, llm_adapter: LLMAdapter, k: int = 3, max_queries: int = 3):
        self.name = name
        self.docs = EmbeddedDocs(embedding_model)
        self.llm_adapter = llm_adapter
        self.k = k
        self.max_queries = max_queries

    def _split(self, queries_str: str) -> list[str]:
        try:
            queries = queries_str.split("\n")
            queries = [query.replace("Query:","").strip() for query in queries]
            return queries
        except:
            return []


    def preprocessing(self, obs: str, state: State) -> None:
        if not obs:
            return
        query_system_prompt = SystemMessage(_rag_query_system_prompt)
        query_user_prompt = UserMessage(f"> {state.get_response()}\n< {obs}")
        queries = self.llm_adapter.generate([query_system_prompt, query_user_prompt])
        queries = self._split(queries)[:self.max_queries]
        results = []
        for query in queries:
            try:
                logger.debug(f"Querying memory with {query}")
                query_results = [result['result'] for result in self.docs.query(query, self.k)]
                results.extend(query_results)
            except:
                pass
        
        self.docs.add_docs([f"> {state.get_response()}\n< {obs}"])

        memory = {"memory": results}
        state.set(self.name, memory)
        logger.info(f"RAGMemory: {results}")

    def postprocessing(self, response: str, state: State) -> None:
        pass

    def reset(self):
        pass


list_memory_entry = """ - ```
  ubuntu-ctf-machine # {hist_cmd}
  {hist_output}
  ```
"""
class ListMemory(Module):
    """Implementing a list memory module that stores the last n commands and their outputs.
    
    The memory is returned as a markdown formatted list of commands and their outputs.
    """

    def __init__(self, name: str, maxlen: None|int = None):
        """
        Args:
            name (str): Name of the memory module.
            maxlen (int): Maximum number of entries to store in memory.
        """
        self.name = name
        self.memory = deque(maxlen=maxlen)

    def preprocessing(self, obs: str, state: State) -> None:
        if obs is None:
            logger.debug("ListMemory: No observation.")
            return
        if obs.strip() == "":
            obs = "> Command ran successfully with no output." 
        if len(obs.split()) > 1000:
            obs = "> Command generated too much output. " \
                    + "Try piping the output of the command in an appropriate filter command." 

        self.memory.append([state.get_response(), obs])

        memory_list = [list_memory_entry.format(hist_cmd=item[0], hist_output=item[1]) for item in self.memory]
        memory_string = "\n".join(memory_list)
        memory_module = {"memory": memory_string}

        state.set(self.name, memory_module)

    def postprocessing(self, response: str, state: State) -> None:
        pass

    def reset(self):
        pass
