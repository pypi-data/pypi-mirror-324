from tinysmith.orchestrator.state import State


class Module:
    """The Module class is an abstract class that defines the interface for all modules.

    Modules are used to preprocess and postprocess the agent's input and output in a reusable
    manner.

    A new module must subclass the Module class and implement the `preprocessing`, 
    `postprocessing`, and `reset` hooks.
    """

    def preprocessing(self, obs: None|str, orchestrator_state: State):
        """Hook that can implement preprocessing of the agent's input of any kind. This is called
        before the PromptEngineer renders the prompt.
        """
        raise NotImplementedError

    def postprocessing(self, response: str, orchestrator_state: State):
        """Hook that can implement postprocessing of the agent's output. This is called before
        PromptEngineer processes the response.
        """
        raise NotImplementedError
    
    def reset(self):
        """Hook that resets the module's state."""
        raise NotImplementedError
