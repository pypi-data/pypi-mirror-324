from json.decoder import JSONDecodeError
import logging

from jinja2.environment import Environment
from jinja2.loaders import PackageLoader

from tinysmith.agent.strategies.planner_reviewer_executor.utils import (
    fill_master_template,
)
from tinysmith.llm.adapters import AssistantMessage, Message, SystemMessage, UserMessage
from tinysmith.llm.utils import json_load_list, json_load_object
from tinysmith.orchestrator.prompting import PromptEngineer
from tinysmith.orchestrator.state import State
from tinysmith.orchestrator.utils import signal_error

logger = logging.getLogger(__name__)



class PlannerPromptEngineer(PromptEngineer):
    def __init__(self):
        self.env = Environment(
                loader=PackageLoader(
                    'tinysmith.agent.strategies.planner_reviewer_executor',
                    'templates'))


    def render_prompt(self, obs: None|str, history: list[Message], orchestrator_state: State) -> None:
        template = self.env.get_template('planner.prompt')
        template_content = {}
        fill_master_template(orchestrator_state, template_content)

        planner_state = orchestrator_state.get('planner')
        if planner_state:
            plan = planner_state.get('plan')
            template_content['plan'] = plan
        
        reviewer_state = orchestrator_state.get('reviewer')
        if reviewer_state and 'feedback' in reviewer_state:
            feedback = reviewer_state.get('feedback')
            feedback_list = [(k, v) for feedback_dict in feedback for k, v in feedback_dict.items()]
            template_content['feedback'] = feedback_list


        prompt = template.render(template_content)
        logger.debug(f'Planner Prompt: {prompt}')
        history.clear()
        history.append(UserMessage(prompt))


    def process_response(self, obs: None|str, response: str, history: list[Message], orchestrator_state: State) -> str:
        try:
            plan = json_load_object(response)
            logger.debug(plan)
            plan = plan["plan"]
        except JSONDecodeError as e:
            signal_error(orchestrator_state, 
                         log_message='Failed parsing planner response json: ' + repr(e),
                         improve_message='Could not parse JSON response. ' + \
                                 'Make sure to respond with only the valid JSON schema outlined above.')
            history.append(AssistantMessage(response))
            return ''
        except KeyError as e:
            signal_error(orchestrator_state, 
                         log_message='Failed parsing planner response json: ' + repr(e),
                         improve_message='Could not parse JSON response. ' + \
                                 'Make sure to respond with only the valid JSON schema outlined above.')
            history.append(AssistantMessage(response))
            return ''


        planner_state = orchestrator_state.get('planner')
        if planner_state is None:
            planner_state = {}
        planner_state['plan'] = plan
        orchestrator_state.set('planner', planner_state)

        task_list = orchestrator_state.get('task_list')
        if task_list is None:
            task_list = []
        orchestrator_state.set('task_list', task_list)
        logger.info(f'Planner Plan: {plan}')
        return response


    def reset(self):
        pass



class ReviewerPromptEngineer(PromptEngineer):
    def __init__(self):
        self.env = Environment(
                loader=PackageLoader(
                    'tinysmith.agent.strategies.planner_reviewer_executor',
                    'templates'))

    def render_prompt(self, obs: None|str, history: list[Message], orchestrator_state: State) -> None:
        template = self.env.get_template('reviewer.prompt')
        template_content = {}
        fill_master_template(orchestrator_state, template_content)

        planner_state = orchestrator_state.get('planner')
        assert planner_state, 'Planner state is missing.'

        plan = planner_state['plan']
        template_content['plan'] = plan

        prompt = template.render(template_content)
        logger.debug(f'Reviewer prompt: {prompt}')
        history.clear()
        history.append(UserMessage(prompt))

    def process_response(self, obs: None|str, response: str, history: list[Message], orchestrator_state: State) -> str:
        try:
            output = json_load_object(response)
        except JSONDecodeError as e:
            signal_error(orchestrator_state,
                         'Failed parsing reviewer response json: ' + repr(e),
                         'Could not parse JSON response. ' + \
                                 'Make sure to respond with only the valid JSON schema outlined above.')
            history.append(AssistantMessage(response))
            return ''

        reviewer_state = orchestrator_state.get('reviewer')
        if reviewer_state is None:
            reviewer_state = {}

        try:
            feedback = output['feedback']
        except KeyError as e:
            signal_error(orchestrator_state,
                         'Invalid response schema: ' + repr(e),
                         'Invalid response JSON schema. Missing [' + repr(e) + ']. ' \
                                 'Make sure to respond with only the valid JSON schema outlined above.')
            history.append(AssistantMessage(response))
            return ''
        if len(feedback) > 0:
            status = 'reject'
        else:
            status = 'accept'
        reviewer_state['status'] = status
        reviewer_state['feedback'] = feedback

        orchestrator_state.set('reviewer', reviewer_state)

        task_list = orchestrator_state.get('task_list')
        if task_list is None:
            task_list = []
        orchestrator_state.set('task_list', task_list)

        logger.info(f'Reviewer feedback: {feedback}')

        return response


    def reset(self):
        pass

# class ExecutorPromptEngineer(PromptEngineer):
#     def __init__(self):
#         self.env = Environment(
#                 loader=PackageLoader(
#                     'tinysmith.agent.strategies.planner_reviewer_executor',
#                     'templates'))
# 
#     def render_prompt(self, obs: None|str, history: list[Message], orchestrator_state: State) -> None:
#         # TODO: change this back to executor.prompt
#         template = self.env.get_template('executor.prompt')
#         template_content = {}
#         fill_master_template(orchestrator_state, template_content)
# 
#         # use few shot template
#         if orchestrator_state.get('is_fewshot'):
#             template_content['few_shot'] = True
#             template = self.env.get_template('few_shot_executor.prompt')
# 
#         executor_state = orchestrator_state.get('executor')
#         if executor_state is None:
#             executor_state = {}
#         else:
#             if obs is not None:
#                 obs = "> Exit code 0." if obs.strip() == "" else obs
#                 # append the observation to the last executed command and add it to state and history
#                 stdout_hist = executor_state['stdout_hist']
#                 stdout_hist[-1].append(obs)
#                 executor_state['stdout_hist'] = stdout_hist
#                 template_content['stdout_hist'] = stdout_hist
#         
#         planner_state = orchestrator_state.get('planner')
#         assert planner_state, 'Planner state is missing.'
# 
#         plan = planner_state['plan']
#         current_task = plan[0]
#         template_content['executor_task'] = current_task
#         executor_state['current_task'] = current_task
# 
#         orchestrator_state.set('executor', executor_state)
# 
#         rag_module_state = orchestrator_state.get('knowledgebase')
#         if rag_module_state and 'knowledge' in rag_module_state:
#             template_content['knowledge'] = rag_module_state['knowledge']
# 
#         prompt = template.render(template_content)
#         logger.debug(f'Executor prompt: {prompt}')
#         history.clear()
#         history.append(UserMessage(prompt))
# 
# 
#     def process_response(self, obs: None|str, response: str, history: list[Message], orchestrator_state: State) -> str:
#         try:
#             output = json_load_object(response)
#         except JSONDecodeError as e:
#             signal_error(orchestrator_state,
#                          'Failed parsing executor response json: ' + repr(e),
#                          'Could not parse JSON response. ' + \
#                                  'Make sure to respond with only the valid JSON schema outlined above. No further text.')
#             history.append(AssistantMessage(response))
#             return ''
# 
#         executor_state = orchestrator_state.get('executor')
#         assert executor_state != None, 'Executor state is missing.'
#         stdout_hist = executor_state.get('stdout_hist')
#         if stdout_hist is None:
#             stdout_hist = []
#         
#         try:
#             status = output['status'].lower()
#             if status == 'progress':
#                 executor_state['status'] = 'progress'
# 
#                 # parse agent output
#                 output['plan'] # make sure 'plan' is in the output
#                 command = output['next']['command']
# 
#                 # update history
#                 stdout_hist.append([command])
#                 executor_state['stdout_hist'] = stdout_hist
# 
#                 # execute step in environment
#                 orchestrator_state.set_is_envstep(True)
#                 logger.debug(f'Executor command: {command}')
#                 return f'{command}'
#             elif status == 'done':
#                 executor_state['status'] = 'done'
# 
#                 # parse agent output
#                 summary = output['summary']
#                 new_interesting_knowledge = output['interesting_knowledge']
# 
#                 # remove the current task from the plan
#                 planner_state = orchestrator_state.get('planner')
#                 assert planner_state, 'Planner state is missing.'
#                 planner_state['plan'].pop(0)
# 
#                 # update task list
#                 task_list = orchestrator_state.get('task_list')
#                 assert task_list != None, 'Task list is missing.'
#                 task_list.append(('Executor/Player', summary))
#                 orchestrator_state.set('task_list', task_list)
#                 
#                 # update interesting knowledge
#                 interesting_knowledge = orchestrator_state.get('interesting_knowledge')
#                 if interesting_knowledge is None:
#                     interesting_knowledge = []
#                 interesting_knowledge.extend(new_interesting_knowledge)
#                 orchestrator_state.set('interesting_knowledge', interesting_knowledge)
# 
#                 # reset the executor's stdout_hist
#                 executor_state['stdout_hist'] = []
# 
#                 logger.info(f'Executor summary: {summary}')
#                 logger.info(f'Executor interesting knowledge: {new_interesting_knowledge}')
#                 return response
#             elif status == 'submit':
#                 executor_state['status'] = 'submit'
#                 flag = output['flag']
#                 logger.info(f'Executor flag: {flag}')
#                 orchestrator_state.set_is_envstep(True)
#                 return f"submit {flag}"
#             else:
#                 signal_error(orchestrator_state,
#                              'Invalid executor status: ' + status,
#                              'Invalid executor status. The status can be either `progress`, `done`, or `submit`. ' + \
#                                  'Make sure to respond with only the valid JSON schema outlined above. No further text.')
#                 history.append(AssistantMessage(response))
#                 return ''
#         except KeyError as e:
#             signal_error(orchestrator_state,
#                          'Invalid response schema: ' + repr(e),
#                          'Invalid response JSON schema. Missing [' + repr(e) + ']. ' \
#                                  'Make sure to respond only the valid JSON schema outlined above. No further text.')
#             history.append(AssistantMessage(response))
#             return ''
#         
#         
#     def reset(self):
#         pass


class ExecutorPromptEngineer(PromptEngineer):
    def __init__(self):
        self.env = Environment(
                loader=PackageLoader(
                    'tinysmith.agent.strategies.planner_reviewer_executor',
                    'templates'))

    def render_prompt(self, obs: None|str, history: list[Message], orchestrator_state: State) -> None:
        # TODO: change this back to executor.prompt
        system_template = self.env.get_template('executor_new.prompt')
        user_template = self.env.get_template('executor_new_user.prompt')
        template_content = {}
        fill_master_template(orchestrator_state, template_content)

        # use few shot template
        if orchestrator_state.get('is_fewshot'):
            template_content['few_shot'] = True
            system_template = self.env.get_template('few_shot_executor_new.prompt')

        executor_state = orchestrator_state.get('executor')
        if executor_state is None:
            executor_state = {}
        else:
            if obs is not None:
                obs = "> Exit code 0." if obs.strip() == "" else obs
                # append the observation to the last executed command and add it to state and history
                stdout_hist = executor_state['stdout_hist']
                stdout_hist[-1].append(obs)
                executor_state['stdout_hist'] = stdout_hist
                template_content['stdout_hist'] = stdout_hist
        
        planner_state = orchestrator_state.get('planner')
        assert planner_state, 'Planner state is missing.'

        plan = planner_state['plan']
        current_task = plan[0]
        template_content['executor_task'] = current_task
        executor_state['current_task'] = current_task

        orchestrator_state.set('executor', executor_state)

        rag_module_state = orchestrator_state.get('knowledgebase')
        if rag_module_state and 'knowledge' in rag_module_state:
            template_content['knowledge'] = rag_module_state['knowledge']

        sys_prompt = system_template.render(template_content)
        user_prompt = user_template.render(template_content)
        logger.debug(f'Executor prompt: {sys_prompt}\n{user_prompt}')
        history.clear()
        history.append(SystemMessage(sys_prompt))
        history.append(UserMessage(user_prompt))


    def process_response(self, obs: None|str, response: str, history: list[Message], orchestrator_state: State) -> str:
        try:
            output = json_load_object(response)
        except JSONDecodeError as e:
            signal_error(orchestrator_state,
                         'Failed parsing executor response json: ' + repr(e),
                         'Could not parse JSON response. ' + \
                                 'Make sure to respond with only the valid JSON schema outlined above. No further text.')
            history.append(AssistantMessage(response))
            return ''

        executor_state = orchestrator_state.get('executor')
        assert executor_state != None, 'Executor state is missing.'
        stdout_hist = executor_state.get('stdout_hist')
        if stdout_hist is None:
            stdout_hist = []
        
        try:
            status = output['status'].lower()
            if status == 'progress':
                executor_state['status'] = 'progress'

                # parse agent output
                output['plan'] # make sure 'plan' is in the output
                command = output['next']['command']

                # update history
                stdout_hist.append([command])
                executor_state['stdout_hist'] = stdout_hist

                # execute step in environment
                orchestrator_state.set_is_envstep(True)
                logger.debug(f'Executor command: {command}')
                return f'{command}'
            elif status == 'done':
                executor_state['status'] = 'done'

                # parse agent output
                summary = output['summary']
                new_interesting_knowledge = output['interesting_knowledge']

                # remove the current task from the plan
                planner_state = orchestrator_state.get('planner')
                assert planner_state, 'Planner state is missing.'
                planner_state['plan'].pop(0)

                # update task list
                task_list = orchestrator_state.get('task_list')
                assert task_list != None, 'Task list is missing.'
                task_list.append(('Executor/Player', summary))
                orchestrator_state.set('task_list', task_list)
                
                # update interesting knowledge
                interesting_knowledge = orchestrator_state.get('interesting_knowledge')
                if interesting_knowledge is None:
                    interesting_knowledge = []
                interesting_knowledge.extend(new_interesting_knowledge)
                orchestrator_state.set('interesting_knowledge', interesting_knowledge)

                # reset the executor's stdout_hist
                executor_state['stdout_hist'] = []

                logger.info(f'Executor summary: {summary}')
                logger.info(f'Executor interesting knowledge: {new_interesting_knowledge}')
                return response
            elif status == 'submit':
                executor_state['status'] = 'submit'
                flag = output['flag']
                logger.info(f'Executor flag: {flag}')
                orchestrator_state.set_is_envstep(True)
                return f"submit {flag}"
            else:
                signal_error(orchestrator_state,
                             'Invalid executor status: ' + status,
                             'Invalid executor status. The status can be either `progress`, `done`, or `submit`. ' + \
                                 'Make sure to respond with only the valid JSON schema outlined above. No further text.')
                history.append(AssistantMessage(response))
                return ''
        except KeyError as e:
            signal_error(orchestrator_state,
                         'Invalid response schema: ' + repr(e),
                         'Invalid response JSON schema. Missing [' + repr(e) + ']. ' \
                                 'Make sure to respond only the valid JSON schema outlined above. No further text.')
            history.append(AssistantMessage(response))
            return ''
        
        
    def reset(self):
        pass
