from django.shortcuts import get_object_or_404
from django.template.context_processors import request

from .models import Script, Project
from .script_data import ScriptData, StepData
from .script_db_manager import Script_db_Manager

class ScriptDataManager:
    def __init__(self, request):
        self.request = request
        self.session = request.session

    def initialize_script_session(self):
        script_data = ScriptData()
        for attribute, value in vars(script_data).items():
            print('---', attribute, value)
            self.session[attribute] = value
        self.session.modified = True

    # edit to take from step_data.py
    def Load_script_seasion_data(self, data_instance, project_id, script_id, version_id):
        session_data = {
            'project': project_id,
            'test_name': data_instance.test_name,
            'type': 'script',
            'steps': [step.to_dict() for step in data_instance.steps],
            'variables': data_instance.variables,
            'script_id': script_id,
            'script_version': version_id
        }
        for key, value in session_data.items():
            self.session[key] = value
        # Mark the session as modified
        self.session.modified = True

    def initialize_automation_architect_session(self):
        self.session['automation_architect_script_name'] = None
        self.session['automation_architect_list'] = []
        self.session.modified = True

    def load_script_to_automation_architect_create_session(self, data_instance, project_id, script_id, version_id):
        script_data = self.Load_script_seasion_data(data_instance, project_id, script_id, version_id)
        self.session['automation_architect_list'].append(script_data)
        self.session.modified = True

    def script_automation_add_script(self):
        print('script_automation_add_script')

    def script_creator_add_or_edit_step(self, form):
        if 'steps' not in self.session:
            raise ValueError("No script initialized in session.")
        print("form.cleaned_data", form.cleaned_data)
        step_id = form.cleaned_data.get('step_id')
        step_data = StepData()

        # Populate step_data with form data
        for key, value in form.cleaned_data.items():
            if hasattr(step_data, key):
                setattr(step_data, key, value)

        step_data.frame_errors['sync'] = form.cleaned_data.get('sync', False)
        step_data.frame_errors['length_plus'] = form.cleaned_data.get('length_plus', False)
        step_data.frame_errors['length_minus'] = form.cleaned_data.get('length_minus', False)
        step_data.frame_errors['sequence_number'] = form.cleaned_data.get('sequence_number', False)
        step_data.frame_errors['checksum'] = form.cleaned_data.get('checksum', False)
        print("data_manager ->", step_data.to_dict())

        if step_id:
            self.session['steps'][step_id - 1] = step_data.to_dict()
        else:
            step_data.step_id = len(self.session['steps']) + 1
            self.session['steps'].append(step_data.to_dict())

        self.session.modified = True

    def save_script(self, user, project):
        # Create and populate a ScriptData instance from session data
        script_data_instance = ScriptData()
        script_data_instance.project = project.id
        script_data_instance.test_name = self.session['test_name']
        script_data_instance.variables = self.session.get('variables', [])

        print(script_data_instance.test_name)
        for steps in self.session['steps']:
            step = StepData()
            step.__dict__.update(steps)
            script_data_instance.steps.append(step)
        if script_data_instance.script_version == None:
            script_data_instance.script_version = 1
        else:
            script_data_instance.script_version = script_data_instance.script_version + 1
        script_data_instance.checksum = script_data_instance.calculate_checksum()
        script_id = self.session.get('editing_script_id')
        db_manager = Script_db_Manager(script_data_instance, project)
        db_manager.save_cript_to_db()
        if script_id:
            script = get_object_or_404(Script, id=script_id, user=user)
        else:
            script = Script(user=user, project=project, test_name=script_data_instance.test_name)
        print("script ===", script)
        print(project.id)

        print("data_manager : script_data_instance:", script_data_instance)
        print("data_manager : script_data_instance-steps:", str(script_data_instance.steps[0].__dict__))

        self.session.pop('editing_script_id', None)
        self.session.modified = True

    def edit_variable(self, index, name, data_type, value):
        if 'variables' in self.session and 0 <= index < len(self.session['variables']):
            self.session['variables'][index] = {
                'name': name,
                'data_type': data_type,
                'value': value
            }
            self.session.modified = True

    def delete_step(self, step_id):
        if 'steps' in self.session:
            self.session['steps'] = [step for step in self.session['steps'] if step['step_id'] != step_id]

            # Reassign step IDs after deletion
            for i, step in enumerate(self.session['steps']):
                step['step_id'] = i + 1
            self.session.modified = True
            return self.session['steps']
        return None

    def move_step(self, step_id, direction):
        if 'steps' in self.session:
            script_steps = self.session['steps']
            index = int(step_id) - 1
            if script_steps[index]['Step_loop_enable'] == True:
                return script_steps
            if direction == 'up' and index > 0:
                if script_steps[index - 1]['Step_loop_enable'] == True:
                    return script_steps
                script_steps[index], script_steps[index - 1] = script_steps[index - 1], script_steps[index]
                script_steps[index]['step_id'], script_steps[index - 1]['step_id'] = script_steps[index - 1]['step_id'], \
                    script_steps[index]['step_id']

            elif direction == 'down' and index < len(script_steps) - 1:
                if script_steps[index + 1]['Step_loop_enable'] == True:
                    return script_steps
                script_steps[index], script_steps[index + 1] = script_steps[index + 1], script_steps[index]
                script_steps[index]['step_id'], script_steps[index + 1]['step_id'] = script_steps[index + 1]['step_id'], \
                    script_steps[index]['step_id']
            for i in script_steps:
                print(i)
            self.session['steps'] = script_steps
            self.session.modified = True
            return script_steps
        return None

    def get_step_from_session(self, step_id):
        try:
            if step_id - 1 < 0 or step_id > len(self.session['steps']):
                return None
            else:
                return self.session['steps'][step_id - 1]
        except:
            raise ValueError("No script initialized in session.")

    def automation_architect_add_step(self):
        print('automation_architect_add_step')

    def add_script_to_automation(self, script_id, version_id):
        # Load and decrypt the full script data
        script = Script.objects.get(id=script_id)
        # project = get_object_or_404(Project, id= request., users= self.request.user)
        manager = Script_db_Manager(script, script.project)

        # Convert ScriptData to a dictionary and include id and type
        decrypted_script_data = manager.load_script_version(version_id).to_dict()
        decrypted_script_data['type'] = 'script'
        decrypted_script_data['id'] = script_id  # Ensure 'id' field is added here
        decrypted_script_data['version_id'] = version_id

        # Add to session list
        if 'automation_architect_list' not in self.session:
            self.session['automation_architect_list'] = []
        self.session['automation_architect_list'].append(decrypted_script_data)
        self.session.modified = True

    def add_delay_to_automation(self, delay):
        # Add a delay to the automation list
        delay_data = {
            'type': 'delay',
            'delay': delay,
        }
        if 'automation_architect_list' not in self.session:
            self.session['automation_architect_list'] = []
        self.session['automation_architect_list'].append(delay_data)
        self.session.modified = True

    def update_step(self, step_id, updated_data):
        if 'steps' not in self.session:
            raise ValueError("No script initialized in session.")
        try:
            step_index = step_id - 1
            self.session['steps'][step_index].update(updated_data)
            self.session.modified = True
            print("all step data", self.session['steps'])
        except IndexError:
            raise ValueError("Step ID out of range.")

    # def validate_neighboring_loops(self, step_id, loop_id):
    #
    #     # Get the loop ID for the current step, default to 0 if None
    #
    #     # Skip validation if the current step is not in a loop
    #     if loop_id > self.session['max_loop_id']+1:
    #         return False
    #
    #     # Define the valid range for neighboring loop IDs
    #     valid_loop_ids = {loop_id - 1, loop_id, loop_id + 1}
    #
    #     # Check the previous step
    #     previous_step = self.get_step_from_session(step_id - 1)
    #     if previous_step:
    #         prev_loop_id = previous_step.get('loop_id') or 0
    #         if prev_loop_id != 0 and prev_loop_id not in valid_loop_ids:
    #             if prev_loop_id == self.session['max_loop_id']:
    #                 return False
    #
    #     # Check the next step
    #     next_step = self.get_step_from_session(step_id + 1)
    #     if next_step:
    #         next_loop_id = next_step.get('loop_id') or 0
    #         if next_loop_id != 0 and next_loop_id not in valid_loop_ids:
    #             if prev_loop_id == self.session['max_loop_id']:
    #                 return False
    #
    #     return True

    def Auto_step_loop_id_detector(self, step_id, loop_id):
        try:
            previous_loop_id = int(self.get_step_from_session(step_id - 1).get('loop_id'))
        except:
            previous_loop_id = 0
        try:
            next_loop_id = int(self.get_step_from_session(step_id + 1).get('loop_id'))
        except:
            next_loop_id = 0

        return_loop_id = 0
        print("prev step -", self.get_step_from_session(step_id - 1))
        print(previous_loop_id, loop_id, next_loop_id)
        print(type(previous_loop_id), type(loop_id))
        if loop_id != 0:
            return_loop_id = loop_id
        elif previous_loop_id != 0 and next_loop_id == 0:
            return_loop_id = previous_loop_id
        elif next_loop_id != 0:
            return_loop_id = next_loop_id
        else:
            print("max loop id ", loop_id)
            return_loop_id = self.session['max_loop_id'] + 1
        self.session['max_loop_id'] = return_loop_id
        return return_loop_id

    def get_script_versions(self, script_id):
        project = get_object_or_404(Project, id=int(self.session['project_id']), users=self.request.user)
        manager = Script_db_Manager(None, project)
        versions = manager.get_script_versions(script_id)
        return versions