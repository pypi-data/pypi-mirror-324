import logging
import os
from datetime import datetime
from urllib import request

from django.conf import settings
from django.contrib import messages  # User feedback system
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied  # Better security exceptions
from django.db import transaction  # Database transaction management
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt


from .forms import ScriptForm, GlobalSettingsForm
from .models import Script, Project
from .seasion_data_manager import ScriptDataManager
from .script_db_manager import Script_db_Manager

from asgiref.sync import async_to_sync
from .script_runner import run_script

# Setup logger
logger = logging.getLogger('automation_views')


@login_required
def global_settings(request):
    """Handle global settings form for script creation."""
    try:
        if request.method == 'POST':
            form = GlobalSettingsForm(user=request.user, data=request.POST)
            if form.is_valid():
                project = form.cleaned_data['project']
                test_name = form.cleaned_data['test_name']

                # Security: Validate user has access to project
                if not project.users.filter(id=request.user.id).exists():
                    raise PermissionDenied("You don't have access to this project")
                else:
                # Initialize session data with timestamp
                    data_manager = ScriptDataManager(request)
                    data_manager.initialize_script_session()
                    request.session['project']= project.id
                    request.session['test_name']= f"{test_name} - Time - {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"
                    request.session['script_version'] = 1
                    request.session.modified = True

                    messages.success(request, 'Global settings saved successfully')
                    return redirect('create_script')
            else:
                messages.error(request, 'Please correct the errors below')
        else:
            form = GlobalSettingsForm(user=request.user)

        return render(request, 'automation/global_settings.html', {'form': form})

    except PermissionDenied as e:
        logger.warning(f"Permission denied for user {request.user.id}: {e}")
        messages.error(request, str(e))
        return redirect('error')
    except Exception as e:
        logger.error(f"Error in global_settings view: {e}")
        messages.error(request, 'An error occurred while processing your request')
        return redirect('error')


@login_required
def create_script(request):

    script_data_manager = ScriptDataManager(request)

    if 'test_name' not in request.session or 'project' not in request.session:
        messages.error(request, 'Please configure global settings first')
        return redirect('global_settings')

    # Get project access
    project_id = request.session['global_settings'].get('project')
    project = get_object_or_404(Project, id=project_id, users=request.user)

    if request.method == 'POST':
        form = ScriptForm(request.POST)
        if form.is_valid():
            # try:
            with transaction.atomic():
                if request.POST.get('action') == 'save':
                    script_data_manager.save_script(request.user, project)
                    messages.success(request, 'Script saved successfully')
                    return redirect('script_list')
                else:
                    script_data_manager.script_creator_add_or_edit_step(form)
                    if request.headers.get('HX-Request'):
                        return render(request, 'partials/script_creation_step_list.html', {
                            'session_script': request.session['steps']
                        })
            # except Exception as e:
            #     print(e)
            #     logger.error(f"Error saving script: {e}")
            #     messages.error(request, 'Error saving script')
            #     return redirect('error')
        else:
            print(form.errors)
            if request.headers.get('HX-Request'):
                return HttpResponseBadRequest('Invalid form data')
            messages.error(request, 'Please correct the form errors')

    # Pass form and session data to the template
    context = {
        'form': ScriptForm(),
        'session_script': request.session.get('steps', []),
        'variables': request.session.get('variables', []),
    }
    return render(request, 'automation/create_script.html', context)

def error(request):
    return render(request, 'automation/error.html')
import logging
logger = logging.getLogger(__name__)

def add_variable(request):
    try:
        logger.debug("Received POST data: %s", request.POST)
        var_name = request.POST.get('var_name')
        data_type = request.POST.get('data_type')
        var_value = request.POST.get('var_value')

        if not (var_name and data_type and var_value):
            logger.error("One or more required fields are missing.")
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        variables = request.session.get('variables', [])
        new_variable = {
            'id': len(variables),
            'name': var_name,
            'data_type': data_type,
            'value': var_value,
        }
        variables.append(new_variable)
        request.session['variables'] = variables
        request.session.modified = True

        return render(request, 'partials/variable_table.html', {'variables': variables})
    except Exception as e:
        logger.exception("Error in add_variable view")
        return JsonResponse({'error': str(e)}, status=500)



@login_required
def edit_variable(request, variable_id):
    new_value = request.POST.get('value')
    new_data_type = request.POST.get('data_type')

    # Retrieve and update the variable in session (or your storage method)
    variables = request.session.get('variables', [])
    for variable in variables:
        if variable['id'] == variable_id:
            if new_value is not None:
                variable['value'] = new_value
            if new_data_type is not None:
                variable['data_type'] = new_data_type
            break
    else:
        return JsonResponse({'error': 'Variable not found'}, status=404)

    request.session['variables'] = variables
    request.session.modified = True

    # Render the updated table
    return render(request, 'partials/variable_table.html', {'variables': variables})
@login_required
def delete_step(request, step_id):
    if request.method == 'POST':
        script_data_manager = ScriptDataManager(request)
        updated_steps = script_data_manager.delete_step(step_id)

        if request.headers.get('HX-Request'):  # Handle HTMX request
            return render(request, 'partials/script_creation_step_list.html', {
                'session_script': updated_steps  # Send updated step list to HTMX
            })

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def load_step(request, step_id):
    script_data_manager = ScriptDataManager(request)
    step_data = script_data_manager.get_step_from_session(step_id)

    if step_data:
        return JsonResponse(step_data)

    return JsonResponse({'error': 'Step not found'}, status=404)


@login_required
def load_script(request):
    print("load_script ->",request)
    if request.method == 'POST':
        script_id = request.POST.get('script_id')
        version_id = request.POST.get('version_id')
        project_id = request.session['project_id']
        if script_id and version_id:
            project = get_object_or_404(Project, id=project_id, users=request.user)
            manager = Script_db_Manager(None, project)
            script_data_instance = manager.load_script_version(script_id , version_id )

            # script = get_object_or_404(Script, id=script_id, user=request.user)

            script_data_manager = ScriptDataManager(request)

            # script_data_instance = manager.load_script_version(int(version_id))

            if script_data_instance:
                # Load global settings and steps into the session
                script_data_manager.Load_script_seasion_data(script_data_instance, project_id, script_id, version_id)

                print("load_script - >",request.session['steps'])
                request.session.modified = True
                return redirect('create_script')

    return redirect('script_list')


@csrf_exempt
def update_step_order(request):
    if request.method == 'POST':
        step_id = request.POST.get('step_id')
        direction = request.POST.get('direction')

        script_data_manager = ScriptDataManager(request)

        updated_steps = script_data_manager.move_step(step_id, direction)
        if updated_steps is not None:
            request.session['steps'] = updated_steps
            request.session.modified = True

            return render(request, 'partials/script_creation_step_list.html', {
                'session_script': updated_steps
            })
        return JsonResponse({'error': 'Step not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def get_script_versions(request):
    print(request)
    script_id = request.GET.get('script_id')
    data_manager = ScriptDataManager(request)
    versions = data_manager.get_script_versions(script_id)
    return render(request, 'partials/version_options.html', {'versions': versions})



def load_scripts(request):
    print("load_scripts ->",request)
    project_id = request.GET.get("project_id")
    request.session['project_id'] = project_id
    project = get_object_or_404(Project, id=project_id, users=request.user)
    manager = Script_db_Manager(None, project)
    project_scripts = manager.get_project_scripts()
    print(project_scripts)
    return render(request, 'partials/script_list_partial.html', {'scripts': project_scripts})


@login_required
def script_list(request):
    user_projects = Project.objects.filter(users=request.user)
    scripts = None
    return render(request, 'automation/script_list.html', {
        'scripts': scripts,
        'projects': user_projects,
    })



def get_environments(request):
    """HTMX view to fetch environments."""
    environments = settings.AUTOMATION_DB_HANDLER.get_environments()
    return render(request, 'partials/script_creation_environment_select.html', {'environments': environments})


def get_components(request, environment_id):
    """HTMX view to fetch components based on the selected environment."""
    components = settings.AUTOMATION_DB_HANDLER.get_components(environment_id)
    return render(request, 'partials/script_creation_component_select.html', {'components': components})


def get_packets(request, component_id):
    """HTMX view to fetch packets based on the selected component."""
    packets = settings.AUTOMATION_DB_HANDLER.get_packets(component_id)
    return render(request, 'partials/script_creation_packet_select.html', {'packets': packets})


def get_parameters(request, packet_id):
    """HTMX view to fetch parameters based on the selected packet."""
    parameters = settings.AUTOMATION_DB_HANDLER.get_parameters(packet_id)
    return render(request, 'partials/script_creation_parameter_select.html', {'parameters': parameters})


def automation_architect(request):
    user_projects = Project.objects.filter(users=request.user)
    selected_project_id = request.GET.get('project_id')

    if selected_project_id:
        selected_project = get_object_or_404(Project, id=selected_project_id, users=request.user)
        scripts = Script.objects.filter(user=request.user, project=selected_project)
    else:
        scripts = None
    request.session['automation_architect_list'] = []
    return render(request, 'automation/automation_architect.html', {
        'scripts': scripts,
        'projects': user_projects,
        'selected_project_id': selected_project_id,
    })


@login_required
def automation_architect_add_script(request):
    print("View 'automation_architect_add_script' called")

    if request.method == 'POST':
        script_id = request.POST.get('script_id')
        version_id = request.POST.get('version_id')
        print("POST data - script_id:", script_id, "version_id:", version_id)

        # Initialize ScriptDataManager and add script to automation
        script_data_manager = ScriptDataManager(request)
        script_data_manager.add_script_to_automation(script_id, version_id)

    # Retrieve updated list from the session and pass it as context
    context = {'automation_acrchitect_script': request.session.get('automation_architect_list', [])}
    print("Rendering 'automation_architect_table.html' with context:", context)
    return render(request, 'partials/automation_architect_table.html', context)


@login_required
def automation_architect_add_delay(request):
    if request.method == 'POST':
        delay = request.POST.get('delay')
        script_data_manager = ScriptDataManager(request)
        # Add the delay to the session list
        script_data_manager.add_delay_to_automation(delay)

    return render(request, 'partials/automation_architect_table.html', {
        'automation_acrchitect_script': request.session.get('automation_architect_list', [])
    })


@login_required
def load_script_variables(request, script_id, instance_id=None):
    # Retrieve Automation Architect scripts from the session
    automation_architect_scripts = request.session.get('automation_architect_list', [])
    print(request.session)
    # Find the specific script instance using both script_id and instance_id
    script_variables = None
    for script in automation_architect_scripts:
        if str(script.get('id')) == str(script_id) and script.get('instance_id') == instance_id:
            script_variables = script.get('variables', [])
            break

    # If no variables are found, initialize with an empty list
    if script_variables is None:
        script_variables = []

    # Pass `script_id` and `instance_id` to the context for identification
    return render(request, 'partials/automation_architecture_variable_table.html', {
        'variables': script_variables,
        'script_id': script_id,
        'instance_id': instance_id
    })


@login_required
def update_session_variable(request, script_id, variable_name):
    # Retrieve the new data_type and/or value from the request
    new_value = request.POST.get('value')
    new_data_type = request.POST.get('data_type')

    # Access Automation Architect scripts in session
    automation_architect_scripts = request.session.get('automation_architect_list', [])

    # Find the specific script and variable to update
    variable_updated = False
    for script in automation_architect_scripts:
        if str(script.get('id')) == str(script_id):
            for variable in script.get('variables', []):
                if variable['name'] == variable_name:
                    # Update the value and data_type if provided
                    if new_value is not None:
                        variable['value'] = new_value
                    if new_data_type is not None:
                        variable['data_type'] = new_data_type
                    variable_updated = True
                    break
            break

    # Save the updated list back to the session if a change was made
    if variable_updated:
        request.session['automation_architect_list'] = automation_architect_scripts
        request.session.modified = True

    # Return a JSON response to confirm the update
    return JsonResponse({
        'success': variable_updated,
        'variable_name': variable_name,
        'new_value': new_value,
        'new_data_type': new_data_type,
    })



from django.http import JsonResponse
def update_step_loop(request):
    if request.method == 'POST':
        script_manager = ScriptDataManager(request)
        step_id = int(request.POST.get('step_id'))
        step_repeat = request.POST.get('step_repeat')
        loop_repeat = request.POST.get('loop_repeat')
        loop_id = int(request.POST.get('loop_id'))
        loop_background = request.POST.get('loop_background') == "on"
        Step_loop_enable = request.POST.get('Step_loop_enable') == "on"

        print("step-enable",type(Step_loop_enable))
        if Step_loop_enable:
            step_data = script_manager.get_step_from_session(step_id)

            # print("prev step -",script_manager.get_step_from_session(step_id-1).get('loop_id'))


            step_data.update({
                'step_repeat': step_repeat,
                'loop_repeat': loop_repeat,
                'loop_id': script_manager.Auto_step_loop_id_detector(step_id, loop_id),
                'loop_background': loop_background,
                'Step_loop_enable': Step_loop_enable,
            })
            script_manager.update_step(step_id, step_data)

            # Render and return the updated step list for HTMX
            return render(request, 'partials/script_creation_step_list.html', {'session_script': request.session['steps']})

        else:
            step_data = script_manager.get_step_from_session(step_id)
            step_data.update({
                'Step_loop_enable': False,
                'loop_id': '0',
            })
            script_manager.update_step(step_id, step_data)

            return render(request, 'partials/script_creation_step_list.html', {'session_script': request.session['steps']})

    return render(request, 'automation/error.html')

def loop_step_repeat_update():
    print('loop_step_repeat_update')

def intro(request):
    return render(request, 'automation/intro.html')


def session_view(request):
    if not request.session.session_key:
        request.session.create()

    session_id = request.session.session_key

    return render(request, 'automation/test.html', {'session_id': session_id})