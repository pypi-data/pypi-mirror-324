
from tinysmith.orchestrator.state import State


def single_agent(observation: None|str, state: State) -> None:
    state.set_agent_name("single_agent")
    state.set_is_envstep(True)
