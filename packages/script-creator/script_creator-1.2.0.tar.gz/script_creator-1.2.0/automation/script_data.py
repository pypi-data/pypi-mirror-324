# Updated script_data.py
import hashlib

class StepData:
    def __init__(self):
        self.step_id = None
        self.loop_id = '0'
        self.loop_repeat = '1'
        self.step_repeat = '1'
        self.loop_background = False
        self.Step_loop_enable = False
        self.environment = None
        self.command = None
        self.sub_command = None
        self.component = None
        self.packet = None
        self.transmition_line = None
        self.parameters = None
        self.value_manipulation = None
        self.operator = None
        self.min_value = None
        self.max_value = None
        self.resolution = None
        self.resolution_value = None
        self.fixed_value = None
        self.enum_value = None
        self.at_time = None
        self.delay = None
        self.value_tolerance = None
        self.value_tolerance_value = None
        self.time_tolerance = None
        self.time_tolerance_value = None
        self.frame_errors = {
            'sync': None,
            'length_plus': None,
            'length_minus': None,
            'sequence_number': None,
            'checksum': None
        }
        self.description = None

        self.script_error_behavior = None

    def to_dict(self):
        return self.__dict__

class ScriptData:
    def __init__(self):
        # Steps
        self.steps = []
        # Global settings attributes
        self.type = 'script'
        self.project = None
        self.test_name = None
        self.script_id = None
        self.script_version = None
        self.max_loop_id = 0
        # Table variables
        self.variables = []

    def validate(self):
        print("no Validation of script data")


    def to_dict(self):
        return {
            'project': self.project,
            'test_name': self.test_name,
            'variables': self.variables,
            'type': self.type,
            'script_version': self.script_version,
            'steps': [step.to_dict() for step in self.steps]
        }
    def calculate_checksum(self):
        data_string = str([step.to_dict() for step in self.steps])
        return hashlib.md5(data_string.encode()).hexdigest()