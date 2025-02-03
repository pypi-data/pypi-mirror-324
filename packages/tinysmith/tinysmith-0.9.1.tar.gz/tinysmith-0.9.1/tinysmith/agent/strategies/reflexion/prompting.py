import logging

from jinja2.environment import Environment
from jinja2.loaders import PackageLoader

from tinysmith.llm.adapters import Message, SystemMessage, UserMessage
from tinysmith.llm.utils import plaintext_load_command
from tinysmith.orchestrator.prompting import PromptEngineer
from tinysmith.orchestrator.state import State
from tinysmith.orchestrator.utils import signal_error

logger = logging.getLogger(__name__)

class ReflectorPromptEngineer(PromptEngineer):
    def __init__(self):
        self.env = Environment(
                loader=PackageLoader(
                    'tinysmith.agent.strategies.reflexion',
                    'templates'))


    def render_prompt(self, obs: None|str, history: list[Message], orchestrator_state: State) -> None:
        template_content = {}
        system_template = self.env.get_template('reflector_system.prompt')
        user_template = self.env.get_template('reflector_user.prompt')

        challenge_description = orchestrator_state.get('challenge_description')
        assert challenge_description, 'Challenge description is missing.'
        template_content['challenge_description'] = challenge_description

        trajectory_memory_state = orchestrator_state.get('reflexion_trajectory')
        if trajectory_memory_state and 'memory' in trajectory_memory_state:
            template_content['trajectory'] = trajectory_memory_state['memory']

        system_prompt = system_template.render(template_content)
        system_msg = SystemMessage(system_prompt)
        user_prompt = user_template.render(template_content)
        user_msg = UserMessage(user_prompt)

        logger.debug(f'Reflector Prompt: {system_prompt}\n{user_prompt}')
        history.clear()
        history.append(system_msg)
        history.append(user_msg)


    def process_response(self, obs: None|str, response: str, history: list[Message], orchestrator_state: State) -> str:
        reflector_state = {'reflection': response}
        orchestrator_state.set('reflector', reflector_state)
        logger.info(f"Reflector: {response}")
        return response

    def reset(self):
        pass



class ActorPromptEngineer(PromptEngineer):
    def __init__(self):
        self.env = Environment(
                loader=PackageLoader(
                    'tinysmith.agent.strategies.reflexion',
                    'templates'))
    def render_prompt(self, obs: None|str, history: list[Message], orchestrator_state: State) -> None:
        system_template = self.env.get_template('actor_system.prompt')
        user_template = self.env.get_template('actor_user.prompt')
        template_content = {}

        # use few shot template
        if orchestrator_state.get('is_fewshot'):
            template_content['few_shot'] = True
            system_template = self.env.get_template('few_shot_simple.prompt')

        challenge_description = orchestrator_state.get('challenge_description')
        assert challenge_description, 'Challenge description is missing.'
        template_content['challenge_description'] = challenge_description

        rag_module_state = orchestrator_state.get('knowledgebase')
        if rag_module_state and 'knowledge' in rag_module_state:
            template_content['knowledge'] = rag_module_state['knowledge']

        lt_memory_state = orchestrator_state.get('reflexion_longterm')
        if lt_memory_state and 'memory' in lt_memory_state:
            template_content['lt_memory'] = lt_memory_state['memory']

        trajectory_memory_state = orchestrator_state.get('reflexion_trajectory')
        if trajectory_memory_state and 'memory' in trajectory_memory_state:
            template_content['trajectory'] = trajectory_memory_state['memory']

        system_prompt = system_template.render(template_content)
        system_msg = SystemMessage(system_prompt)
        user_prompt = user_template.render(template_content)
        user_msg = UserMessage(user_prompt)

        logger.debug(f'Actor Prompt: {system_prompt}\n{user_prompt}')
        history.clear()
        history.append(system_msg)
        history.append(user_msg)


    def process_response(self, obs: None|str, response: str, history: list[Message], orchestrator_state: State) -> str:
        logger.debug(f"Actor: {response}")
        command = plaintext_load_command(response)
        if not command:
            eval_info = orchestrator_state.get('evaluation')
            if eval_info is None:
                eval_info = {}
            eval_info['current_step'] = eval_info.get('current_step', 0) + 1
            signal_error(orchestrator_state, 
                         log_message="No valid command in response.", 
                         improve_message="Invalid response." \
                                 + "Either multiple commands were detected or no command was found. "\
                                 + "Please use the schema provided above. "\
                                 + "The final line of your response *must* contain `Command: <your bash command>`")
            return ''
        # Signal environment step
        orchestrator_state.set_is_envstep(True)
        
        # Store information for evaluator heuristic
        eval_info = orchestrator_state.get('evaluation')
        if eval_info is None:
            eval_info = {}
        eval_info['last_command'] = eval_info.get('current_command')
        eval_info['current_command'] = command
        orchestrator_state.set('evaluation', eval_info)

        return command

    def reset(self):
        pass
