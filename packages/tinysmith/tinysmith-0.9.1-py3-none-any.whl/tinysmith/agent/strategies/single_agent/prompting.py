
import logging

from jinja2.environment import Environment
from jinja2.loaders import PackageLoader

from tinysmith.llm.adapters import Message, SystemMessage, UserMessage
from tinysmith.llm.utils import plaintext_load_command
from tinysmith.orchestrator.prompting import PromptEngineer
from tinysmith.orchestrator.state import State
from tinysmith.orchestrator.utils import signal_error

logger = logging.getLogger(__name__)


class SingleAgentPromptEngineer(PromptEngineer):
    def __init__(self):
        self.jinja = Environment(
                loader=PackageLoader(
                    'tinysmith.agent.strategies.single_agent',
                    'templates'))


    def render_prompt(self, obs: None|str, history: list[Message], orchestrator_state: State) -> None:
        system_template = self.jinja.get_template('system.prompt')
        user_template = self.jinja.get_template('user.prompt')
        template_content = {}

        # use few shot template
        if orchestrator_state.get('is_fewshot'):
            template_content['few_shot'] = True
            system_template = self.jinja.get_template('few_shot_simple.prompt')

        challenge_description = orchestrator_state.get('challenge_description')
        assert challenge_description, 'Challenge description is missing.'
        template_content['challenge_description'] = challenge_description

        rag_module_state = orchestrator_state.get('knowledgebase')
        if rag_module_state and 'knowledge' in rag_module_state:
            template_content['knowledge'] = rag_module_state['knowledge']

        memory_module_state = orchestrator_state.get('list_memory')
        if memory_module_state and 'memory' in memory_module_state:
            template_content['trajectory'] = memory_module_state['memory']

        system_prompt = system_template.render(template_content)
        system_msg = SystemMessage(system_prompt)
        user_prompt = user_template.render(template_content)
        user_msg = UserMessage(user_prompt)

        logger.debug(f'Agent Prompt: {system_prompt}\n{user_prompt}')
        history.clear()
        history.append(system_msg)
        history.append(user_msg)


    def process_response(self, obs: None|str, response: str, history: list[Message], orchestrator_state: State) -> str:
        logger.debug(f"Agent: {response}")

        command = plaintext_load_command(response)
        if not command:
            signal_error(orchestrator_state, 
                         log_message="No valid command in response.", 
                         improve_message="Invalid response." \
                                 + "Either multiple commands were detected or no command was found. "\
                                 + "Please use the schema provided above. "\
                                 + "The final line of your response *must* contain `Command: <your bash command>`")
            return ''
        orchestrator_state.set_is_envstep(True)
        return command


    def reset(self):
        pass
