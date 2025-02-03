import logging

from tinysmith.agent.agent import Agent
from tinysmith.orchestrator.state import State
from tinysmith.orchestrator import TransitionFunction

logger = logging.getLogger(__name__)



class Orchestrator:
    def __init__(self, 
                 agents: None|list[Agent] = None, 
                 transition: None|TransitionFunction = None,
                 state: None|State = None) -> None:
        """The orchestrator manages the multi-agent system that represents a strategy to solve a problem. The Orchestrator class is the central class that manages the meta state of the agents and their interactions. It is responsible for calling the agents according to the transition function and passes around a global state object. 

        The agents represent parts of the multi-agent system, and are registered with the orchestrator. The orchestrator calls the agents according to the transition function. 
        The transition function decides what agent is called next. It is a callback that receives the last environment observation and the current state object.
        The state object is passed around between agents and is used for cross-agent communication.

        Args:
            agents: A list of agents to be registered with the orchestrator. This list comprises all actors in the multi-agent system.
            transition: The transition function that decides what agent is called next. It is a callback that receives the last environment observation and the current state. 
            state: The global state object that is passed around between agents.
        """
        self.agents = agents if agents else []
        self.transition = transition
        self.state = state if state else State()


    def register_agent(self, agent: Agent) -> None:
        """
        Register an agent with the orchestrator. The orchestrator will call the agents according to the transition function.
        Args:
            agent: The agent to be registered.
        """
        self.agents.append(agent)


    def register_transition(self, func: None|TransitionFunction) -> None:
        """
        Register the transition function. The transition function is a callback that receives the last environment observation and the current state. Decides what agent is called next. Defines cross-agent communication through the state object.

        Args:
            func:
                str: Environment observation or None if there is none.
                State: The current state of the orchestrator. Is used by agents to communicate.
        """
        self.transition = func


    def forward(self, obs: None|str, reward: int|None) -> str:
        """
        Runs the orchestrator's agents according to the transition function, until the environment step is requested.
        Returns the executing agent's output.

        Args:
            obs: observation provided by the environment
            reward: reward provided by the environment 
        Returns the final response for the environment.
        """
        if not self.transition:
            raise ValueError("Must register transition before calling forward.")
        if len(self.agents) == 0:
            raise ValueError("Must register at least one agent before calling forward.")

        errors = 0
        while True:
            if errors >= self.state.get_max_errors():
                raise OverflowError("Too many errors encountered.")

            if self._error_handling():
                # in case of error, skip the transition and try again with improvement message
                errors += 1
            else:
                self.transition(obs, self.state)
                errors = 0

            logger.debug(f"Current state: {self.state.get_agent_name()}")
            next_agent = [agent for agent in self.agents if agent.name == self.state.get_agent_name()][0]
            response = next_agent.forward(obs, reward, self.state)
            self.state._internal['response'] = response
            if self.state.get_is_envstep():
                logger.debug("Environment step requested.")
                break
            obs = None
        self.state.set_is_envstep(False)
        return response


    def reset(self, state: None|State = None):
        """The reset function resets the orchestrator and all agents."""
        for agent in self.agents:
            agent.reset()
        self.state = state if state else State()


    def _error_handling(self) -> bool:
        """The orchestrator must handle agent errors. If any component in the system signals a
        misbehaved agent response, the signal is logged here. The orchestrator skips the transition
        in the main forward loop.
        """
        if self.state.get_error_status():
            assert self.state.get_error_log_message() is not None, "Error log message is missing."
            agent_name = self.state.get_agent_name()
            log_message = self.state.get_error_log_message()
            logger.info(f"Agent parsing error: [{agent_name}]/{log_message}")
            logger.debug(f"Improvement message: {self.state.get_error_improve_message()}")
            assert self.state.get_error_improve_message() is not None, "Error message for agent improvement is missing."
            return True
        return False



