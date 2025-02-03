from tinysmith.orchestrator.state import State

def fill_master_template(state: State, template_content: dict) -> None:
        challenge_description = state.get('challenge_description')
        assert challenge_description, 'Challenge description is missing.'
        template_content['challenge_description'] = challenge_description

        task_list = state.get('task_list')
        if task_list:
            template_content['task_list'] = task_list

        interesting_knowledge = state.get('interesting_knowledge')
        if interesting_knowledge:
            template_content['interesting_knowledge'] = interesting_knowledge
