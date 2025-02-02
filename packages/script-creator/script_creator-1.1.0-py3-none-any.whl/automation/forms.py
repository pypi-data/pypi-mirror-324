from django import forms
from .models import Project
from .data_db_manager import AutomationDBHandler
from django.conf import settings
import os


class ScriptForm(forms.Form):
    OPERATION_CHOICES = [
        ('set', 'set'),
        ('get', 'get'),
        ('general', 'general'),
    ]

    SUB_COMMAND_CHOICES = [
        ('sub_command_1', 'Sub Command 1'),
        ('sub_command_2', 'Sub Command 2'),
        ('sub_command_3', 'Sub Command 3'),
    ]

    VALUE_MANIPULATION_CHOICES = [
        ('no-change', 'No Change'),
        ('fixed', 'Fixed Value'),
        ('random', 'Random Value'),
        ('enum', 'Enum'),
        ('Parameters', 'Parameters')
    ]

    OPERATOR_CHOICES = [
        ('=', '='),
        ('+', '+'),
        ('-', '-'),
        ('*', '*'),
        ('/', '/'),

    ]

    TOLERANCE_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed')
    ]

    TIME_TOLERANCE_CHOICES = [
        ('reach-value', 'Time to Reach Value'),
        ('stable-value', 'Period of Stable Value')
    ]

    TRANSMITION_LINE = [
        ('HW', 'HW'),
        ('SW', 'SW'),
    ]
    SCRIPT_ERROR_BEHAVIOR = [
        ('pause', 'pause on error'),
        ('repeat', 'repeat on error'),
        ('break', 'break on error'),
        ('continue', 'continue on error(default)'),
    ]

    # Static fields
    command = forms.ChoiceField(choices=OPERATION_CHOICES, label="Operation")
    sub_command = forms.ChoiceField(choices=SUB_COMMAND_CHOICES, label="Sub Command")
    transmition_line = forms.ChoiceField(choices=TRANSMITION_LINE, label="TTC")
    operator = forms.ChoiceField(choices=OPERATOR_CHOICES, label="Operator")
    value_manipulation = forms.ChoiceField(choices=VALUE_MANIPULATION_CHOICES, label="Value Manipulation")

    # Other fields
    fixed_value = forms.FloatField(required=False, label="Fixed Value")
    min_value = forms.FloatField(required=False, label="Min Value")
    max_value = forms.FloatField(required=False, label="Max Value")
    resolution = forms.ChoiceField(choices=TOLERANCE_TYPE_CHOICES, required=False, label="Resolution Type")
    resolution_value = forms.FloatField(required=False, label="Resolution Value")
    enum_value = forms.CharField(max_length=100, required=False, label="Enum Value")
    table_parameters = forms.ChoiceField(choices=[], required=False, label="Table Parameters")

    step_id = forms.IntegerField(widget=forms.HiddenInput(), required=False, label="Step ID")
    at_time = forms.FloatField(required=False, label="At Time")
    delay = forms.FloatField(required=False, label="Delay")

    # Boolean fields
    sync = forms.BooleanField(required=False, label="Sync")
    length_plus = forms.BooleanField(required=False, label="Length Plus")
    length_minus = forms.BooleanField(required=False, label="Length Minus")
    sequence_number = forms.BooleanField(required=False, label="Sequence Number")
    checksum = forms.BooleanField(required=False, label="Checksum")
    script_error_behavior = forms.ChoiceField(choices=SCRIPT_ERROR_BEHAVIOR, required=True)

    value_tolerance = forms.ChoiceField(choices=TOLERANCE_TYPE_CHOICES, label="Value Tolerance")
    value_tolerance_value = forms.FloatField(required=False)
    time_tolerance = forms.ChoiceField(choices=TIME_TOLERANCE_CHOICES, label="Time Tolerance")
    time_tolerance_value = forms.FloatField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description")

    # Define form fields
    environment = forms.ChoiceField(choices=[], label="Environment", required=False)
    component = forms.ChoiceField(choices=[], label="Component", required=False)
    packet = forms.ChoiceField(choices=[], label="Packet", required=False)
    parameters = forms.ChoiceField(choices=[], label="Parameters", required=False)

    def __init__(self, *args, **kwargs):
        super(ScriptForm, self).__init__(*args, **kwargs)

        # Load environments using the centralized AutomationDBHandler from settings
        db_handler = settings.AUTOMATION_DB_HANDLER
        environments = db_handler.get_environments()
        self.fields['environment'].choices = [('', 'Select Environment')] + [
            (str(env['id']), env['name']) for env in environments
        ]

        # Load dependent choices based on provided data
        if args and args[0]:  # args[0] contains POST data
            self.populate_dependent_fields(args[0])

    def populate_dependent_fields(self, data):
        """Populate dependent fields based on selected values."""
        # Load components if environment is selected
        env_id = data.get('environment')
        if env_id:
            components = settings.AUTOMATION_DB_HANDLER.get_components(int(env_id))
            self.fields['component'].choices = [('', 'Select Component')] + [
                (str(comp['id']), comp['name']) for comp in components
            ]

            # Load packets if component is selected
            comp_id = data.get('component')
            if comp_id:
                packets = settings.AUTOMATION_DB_HANDLER.get_packets(int(comp_id))
                self.fields['packet'].choices = [('', 'Select Packet')] + [
                    (str(packet['id']), packet['name']) for packet in packets
                ]

                # Load parameters if packet is selected
                packet_id = data.get('packet')
                if packet_id:
                    parameters = settings.AUTOMATION_DB_HANDLER.get_parameters(int(packet_id))
                    self.fields['parameters'].choices = [('', 'Select Parameter')] + [
                        (str(param['id']), param['name']) for param in parameters
                    ]
        else:
            # Set empty choices for dependent fields if no selections are made
            self.fields['component'].choices = [('', 'Select Component')]
            self.fields['packet'].choices = [('', 'Select Packet')]
            self.fields['parameters'].choices = [('', 'Select Parameter')]

    def get_choice_display(self, field_name, value):
        """Utility to get display name for a selected value from field choices."""
        field = self.fields.get(field_name)
        if field:
            return dict(field.choices).get(value, "")
        return ""

    def clean(self):
        cleaned_data = super().clean()
        # Validate cascading dependencies within the form
        if cleaned_data.get('environment') and not cleaned_data.get('component'):
            self.add_error('component', 'Component is required when environment is selected.')
        if cleaned_data.get('component') and not cleaned_data.get('packet'):
            self.add_error('packet', 'Packet is required when component is selected.')
        if cleaned_data.get('packet') and not cleaned_data.get('parameters'):
            self.add_error('parameters', 'Parameters are required when packet is selected.')

        return cleaned_data


# Keep your existing GlobalSettingsForm unchanged
class GlobalSettingsForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.none(), label="Select Project")
    test_name = forms.CharField(max_length=100, required=True)
    Requirment_id = forms.CharField(max_length=100, required=False)

    def __init__(self, user, *args, **kwargs):
        super(GlobalSettingsForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(users=user)
