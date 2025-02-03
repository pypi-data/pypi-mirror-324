import logging

from tinysmith.orchestrator.state import State

logger = logging.getLogger(__name__)


def signal_error(state: State, log_message: str, improve_message: str) -> None:
    """PromptEngineers and transition functions can signal an error to the orchestrator.
    This prompts a retry of the current agent with the improve message.

    log_message: a message that will be logged
    improve_message: this message shall be used by the PromptEngineer to improve the agent's response
    """
    state.set_error_status(True)
    state.set_error_log_message(log_message)
    state.set_error_improve_message(improve_message)

