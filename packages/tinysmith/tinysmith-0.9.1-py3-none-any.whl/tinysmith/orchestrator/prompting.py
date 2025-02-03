from tinysmith.llm.adapters import Message
from tinysmith.orchestrator.state import State

# TODO: refactor this to ABC

class PromptEngineer:
    """The PromptEngineer object steers the behavior of an agent.

    To implement a new agent, you must subclass the PromptEngineer and implement the
    `render_prompt`, `process_response`, and `clean` methods.
    """

    def render_prompt(self, obs: None|str, history: list[Message], orchestrator_state: State) -> None:
        """
        Hook that renders the agent's prompt. Creates a history view that will be passed to the LLM as a prompt.

        An implementation of this method must react to the environment observation or information of other components in the state object.

        The method shapes the agent's behaviour by building the `history` list. The `history` list is a list of tinysmith Message objects that describe the full prompt for the LLM.
        """
        raise NotImplementedError

    def process_response(self, obs: None|str, response: str, history: list[Message], orchestrator_state: State) -> str:
        """
        Hook that parses and manipulates the response. 
        
        An implementation of this method can parse the LLM `response`. Extracted information can
        be stored in the state object.

        The final response can be edited and must be returned as a string.
        """
        raise NotImplementedError

    def reset(self):
        """Hook that resets the agent's state. 

        An implementation of this method must reset all internal state.
        """
        raise NotImplementedError
