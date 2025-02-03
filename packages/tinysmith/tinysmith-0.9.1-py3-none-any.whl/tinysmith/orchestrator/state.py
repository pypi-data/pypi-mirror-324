
# TODO: The state object is used with dictionaries as namespaces per 
# Module / PromptEngineer, by convention. We should make this part of the API. 

class State:
    """The global state object. It is passed around between agents and framework components and is used for cross-agent communication. It is a dictionary-like object that can store arbitrary key-value pairs. 

    The state object is used to store information that is shared between agents. A well-working convention when designing strategies with multiples agents and modules is to namespace each component and store its state as a dict in the state object:

    ```
    # Set
    agent1_state = {}
    agent1_state.set('key', 'value')
    state.set('agent1', agent1_state)

    # Get
    agent1_state = state.get('agent1')
    assert agent1_state is not None, "Agent1 state is missing."
    agent1_state.get('key', "default value")
    ```

    The global state object is additionally used to store framework metadata that can be used
    through the objects getter/setter API.
    """
    def __init__(self):
        self._internal = {
            'env_step': False, # signals that we want to take a step in the env
            'agent_name': 'init', # name of the last agent to respond
            'response': None, # last agent's response
            'error': { # error state
                'is_error': False,
                'log_message': None,
                'improve_message': None
                } 
        }
        self._state = {}

    def get_is_envstep(self):
        """Returns the environment step flag. If True, the orchestrator will request an environment step."""
        return self._internal['env_step']

    def set_is_envstep(self, value: bool):
        """Sets the environment step flag. If True, the orchestrator will request an environment step."""
        self._internal['env_step'] = value

    def get_agent_name(self) -> str:
        """Returns the name of the last agent that responded.
        This can be used to determine the next agent to call in the transition function.
        """
        return self._internal['agent_name']

    def set_agent_name(self, value: str):
        """Sets the name of the next agent that should be called.
        This can be used to set the next agent to call in the transition function.
        """
        self._internal['agent_name'] = value

    def get_response(self) -> str:
        """Returns the last executor's response.

        N.B.: This is the last executor's response. If a non-executor agent has responded 
        in the meantime, this value will be null to avoid confusion.
        """
        return self._internal['response']

    def set_error_status(self, is_error: bool):
        """Sets the error status. If True, the orchestrator will skip the transition and try again
        with an improvement message.
        
        Use the `orchestrator.utils.signal_error` function for an easy helper function for 
        error handling.
        """
        self._internal['error']['is_error'] = is_error

    def get_error_status(self) -> bool:
        """Returns the error status. If True, the orchestrator will skip the transition and try
        again with an improvement message.

        Use the `orchestrator.utils.signal_error` function for an easy helper function for 
        error handling.
        """
        return self._internal['error']['is_error']

    def set_error_log_message(self, message: str):
        self._internal['error']['log_message'] = message

    def get_error_log_message(self) -> str:
        return self._internal['error']['log_message']

    def set_error_improve_message(self, message: str):
        self._internal['error']['improve_message'] = message

    def get_error_improve_message(self) -> str:
        return self._internal['error']['improve_message']

    def reset_error(self):
        """Resets the error state. This is automatically called by the agent after re-prompting.

        Don't use this if you are not sure what you are doing!
        """
        self._internal['error'] = {
                'is_error': False,
                'log_message': None,
                'improve_message': None
                } 

    def get_max_errors(self) -> int:
        """Returns the maximum number of errors that can be encountered before the orchestrator
        raises an exception.
        """
        # TODO: remove this assert if we want to make this a default value of 3
        assert self._internal.get('max_errors') is not None, "Max errors is missing."
        return self._internal.get('max_errors', 3)

    def set_max_errors(self, value: int):
        """Sets the maximum number of errors that can be encountered before the orchestrator
        raises an exception.
        """
        self._internal['max_errors'] = value

    def set_max_steps(self, value: int):
        """Sets the maximum number of steps that the orchestrator can take before
        raising an exception.

        This can be used to stop the system after a pre-defined number of steps. The environment
        or the agent-env loop can independently set a stopping criterion.
        """
        self._internal['max_steps'] = value

    def get_max_steps(self) -> int:
        """Returns the maximum number of steps that the orchestrator can take before
        raising an exception.

        This can be used to stop the system after a pre-defined number of steps. The environment
        or the agent-env loop can independently set a stopping criterion.
        """
        return self._internal.get('max_steps')
    
    def get(self, key: str):
        """Generic API for getting a value from the state object.

        This is the main API for reading the state object. The state object is a dictionary-like
        object that can store arbitrary key-value pairs.
        """
        return self._state.get(key)

    def set(self, key: str, value):
        """Generic API for setting a value in the state object.

        This is the main API for writing to the state object. The state object is a dictionary-like
        object that can store arbitrary key-value pairs.
        """
        self._state[key] = value

    def __repr__(self):
        return f"{self._state}"


