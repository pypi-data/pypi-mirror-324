import logging

from distance import nlevenshtein

from tinysmith.orchestrator.state import State

logger = logging.getLogger(__name__)

def _evaluator(observation: None|str, state: State) -> bool:
    # Evaluation Heuristic
    # - if the wrong flag was submitted
    # - if the actor is repeating a similar command more than 3 times
    # - if the max_steps is reached
    # - if an error has occurred
    eval_info = state.get('evaluation')
    if eval_info is None:
        eval_info = {}
    else:
        if eval_info.get('error_occurred', False):
            logger.info("Evaluator: Needs reflection. Error occurred.")
            return True

        # Check if the max steps is reached
        logger.debug(f"Current step: {eval_info.get('current_step', 0)}")
        logger.debug(f"Max steps: {state.get_max_steps()}")
        if eval_info.get('current_step', 0) == state.get_max_steps()-1:
            logger.info("Evaluator: Needs reflection. Max steps reached.")
            return True

        # Distance between the last two commands
        last_command = eval_info.get('last_command')
        current_command = eval_info.get('current_command')
        if last_command is None or current_command is None:
            logger.debug("Evaluator: No previous command to compare.")
            return False
        distance = nlevenshtein(last_command, current_command)

        if distance == 0.0:
            logger.info(f"Evaluator: Needs reflection. Repeating the same command. {last_command}, {current_command}, {distance}")
            eval_info['last_command'] = None
            return True
        elif distance < 0.2:
            if eval_info.get('num_same_command', 0) >= 3:
                logger.info(f"Evaluator: Needs reflection. Repeating the same command. {last_command}, {current_command}, {distance}")
                eval_info['last_command'] = None
                return True
            else:
                logger.debug("Evaluator: Repeating the same command... Heuristic not yet triggered.")
                eval_info["num_same_command"] = eval_info.get('num_same_command', 0) + 1

    state.set('evaluation', eval_info)
    return False


def reflexion(observation: None|str, state: State) -> None:
    if state.get_agent_name() == "init":

        # Initialize the evaluation info
        _evaluator(observation, state)
        eval_info = state.get('evaluation')
        assert eval_info is not None, "Evaluation info is missing."

        eval_info['current_step'] = eval_info.get('current_step', 0) + 1
        state.set_agent_name("actor")

    elif state.get_agent_name() == "reflector":
        eval_info = state.get('evaluation')
        assert eval_info is not None, "Evaluation info is missing."
        eval_info['current_step'] = eval_info.get('current_step', 0) + 1
        state.set_agent_name("actor")

    elif state.get_agent_name() == "actor":
        needs_reflection = _evaluator(observation, state)
        
        if needs_reflection:
            state.set_agent_name("reflector")
        else:
            eval_info = state.get('evaluation')
            assert eval_info is not None, "Evaluation info is missing."
            eval_info['current_step'] = eval_info.get('current_step', 0) + 1

            state.set_agent_name("actor")
    else:
        raise ValueError("Unknown agent name: {}".format(state.get_agent_name()))
