import logging

from tinysmith.orchestrator.state import State
from tinysmith.orchestrator.utils import signal_error

logger = logging.getLogger(__name__)

# TODO: PromptEngineers, transition function should be handled as a `Strategy` object. That object validates metadata: 
#   - are enough agents registered
#   - do the agents have the correct names
#   - which modules can/should be registered?

done_json_scheme = """
### Output Format
You can not use `"status": "progress"` anymore. Use the following schema to signal that you are done:
```
{
    "status": "done",
    "summary": "<A detailed summary for your teammates, of what you accomplished>"
    "interesting_knowledge": [
        "<A full comprehensive list of all interesting observations you made during your task>"
        ...
    ]
}
```
"""

def planner_reviewer_executor(observation: None|str, state: State) -> None:
    # the orchestrator was initialized
    if state.get_agent_name() == "init":
        state.set_agent_name("planner")

    elif state.get_agent_name() == "planner":
        # planner has created a plan
        state.set_agent_name("reviewer")

    elif state.get_agent_name() == "reviewer":
        reviewer_state = state.get("reviewer")
        assert reviewer_state is not None, "Reviewer state is missing."

        status = reviewer_state['status']

        # reviewer can only reject 'max_rejects' times
        if reviewer_state.get('max_rejects'):
            reviewer_num_rejects = reviewer_state.get('num_rejects', 0)
            if reviewer_num_rejects >= reviewer_state['max_rejects']:
                logger.info("Reviewer reached max rejects. Setting status to accept.")
                status = 'accept'

        # an accepted plan goes to the executor
        if status == "accept":
            reviewer_state['num_rejects'] = 0
            state.set('reviewer', reviewer_state)
            state.set_agent_name("executor")
        # a rejected plan goes back to the planner
        elif status == "reject":
            reviewer_state['num_rejects'] = reviewer_state.get('num_rejects', 0) + 1
            logger.debug(f"Reviewer rejected the plan. Number of rejects: {reviewer_state['num_rejects']}")
            state.set('reviewer', reviewer_state)
            state.set_agent_name("planner")
        # if the status is invalid, the reviewer is called again with an error message
        else:
            signal_error(state, 
                         "Invalid reviewer status", 
                         "Invalid reviewer status. The status can be either `accept` or `reject`. " + \
                                 "Make sure to use the valid schema outlined above.")

    elif state.get_agent_name() == "executor":
        executor_state = state.get('executor')
        assert executor_state is not None, "Executor state is missing."

        # If the executor reaches its max steps we signal it via a response that it should 
        # set its status to done and submit a summary
        if executor_state.get('max_steps'):
            executor_num_steps = executor_state.get('num_steps', 0)
            logger.debug(f"Executor steps: {executor_num_steps}")
            if executor_num_steps == executor_state['max_steps']:
                logger.info("Executor reached max steps.")
                signal_error(state,
                             "Executor reached max steps. Signalling the agent to stop.",
                             "You reached your maximum number of steps. " \
                                     + "Please set your status to `done` and submit a detailed " \
                                     + "summary of what you found out and add all interesting " \
                                     + "information, especially what confused you and where " \
                                     + "you got stuck. Make sure your team captain understands " \
                                     + "what they need to change in the plan to solve this challenge" \
                                     + done_json_scheme)
            elif executor_num_steps > executor_state['max_steps']:
                executor_state['status'] = 'done'


        if executor_state['status'] == "progress":
            # executor continues until the task is done
            executor_state['num_steps'] = executor_state.get('num_steps', 0) + 1
            state.set('executor', executor_state)
            state.set_agent_name("executor")
        elif executor_state['status'] == "done":
            # when the task is done, the reviewer decides whether a new plan is needed
            executor_state['num_steps'] = 0
            state.set('executor', executor_state)
            state.set_agent_name("reviewer")
        else:
            signal_error(state, 
                         "Invalid executor status", 
                         "Invalid executor status. The status can be either `progress`, `done`, or `submit`. " + \
                         "Make sure to use the valid schema outlined above.")

    else:
        raise ValueError(f"Invalid status: {state.get_agent_name()}")
