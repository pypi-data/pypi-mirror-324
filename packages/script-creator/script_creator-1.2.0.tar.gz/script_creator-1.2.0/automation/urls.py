from django.urls import path

from . import views

urlpatterns = [
    path('global_settings/', views.global_settings, name='global_settings'),
    path('create_script/', views.create_script, name='create_script'),
    path('scripts/', views.script_list, name='script_list'),
    path('intro/', views.intro, name='intro'),
    path('load_script/', views.load_script, name='load_script'),
    path('delete_step/<int:step_id>/', views.delete_step, name='delete_step'),
    path('load_step/<int:step_id>/', views.load_step, name='load_step'),
    path('update_step_order/', views.update_step_order, name='update_step_order'),
    path('get_script_versions/', views.get_script_versions, name='get_script_versions'),
    path('add-variable/', views.add_variable, name='add_variable'),
    path('edit_variable/<int:variable_id>/', views.edit_variable, name='edit_variable'),
    path('error/', views.error, name='error'),
    path('htmx/get-components/<int:environment_id>/', views.get_components, name='get_components'),
    path('htmx/get-packets/<int:component_id>/', views.get_packets, name='get_packets'),
    path('htmx/get-parameters/<int:packet_id>/', views.get_parameters, name='get_parameters'),
    path('get-environments/', views.get_environments, name='get_environments'),
    path('load-scripts/', views.load_scripts, name='load_scripts'),
    path('automation-architect/', views.automation_architect, name='automation_architect'),
    path('automation-architect-add-script/', views.automation_architect_add_script,
         name='automation_architect_add_script'),
    path('automation-architect-add-delay/', views.automation_architect_add_delay,
         name='automation_architect_add_delay'),
    path('load-script-variables/<int:script_id>/<str:instance_id>/', views.load_script_variables,
         name='load_script_variables'),
    path('update-session-variable/<int:script_id>/<str:variable_name>/', views.update_session_variable,
         name='update_session_variable'),
    path('update_step_loop/', views.update_step_loop, name='update_step_loop'),
    path('session_view/', views.session_view, name='session_view'),

]