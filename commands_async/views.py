# coding=utf-8
import collections
from celery.task.control import revoke
from django.core.exceptions import PermissionDenied

from django.http import JsonResponse
from django.views.generic import FormView, View
from celery.result import AsyncResult
from .forms import TaskForm
from django.core.management import get_commands
from commands_async.tasks import command_exec
from celery import current_app
from . import settings


class TaskFormView(FormView):
    """ Task execution form """

    template_name = "cmdasync/index.html"

    form_class = TaskForm
    success_url = '.'

    commands_skip = settings.COMMANDS_ASYNC_COMMANDS_IGNORE

    def is_command_valid(self, command_name, app_name=None):
        items = [command_name]
        if app_name is not None:
            items.append(app_name + "." + command_name)
        return all(map(lambda x: x not in self.commands_skip, items))

    def get_context_data(self, **kwargs):
        context = super(TaskFormView, self).get_context_data(**kwargs)

        commands = collections.OrderedDict()
        commands_all = get_commands()

        # merge
        for command_name in commands_all:
            app_name = commands_all[command_name]
            items = commands.setdefault(app_name, [])
            if self.is_command_valid(command_name, app_name=app_name):
                items.append(command_name)

        # order
        for key in commands:
            commands[key].sort()

        context['commands'] = commands
        context['settings'] = settings
        return context

    def form_invalid(self, form):
        return JsonResponse({
            'form': {
                'errors': form.errors
            }
        }, status=400)

    def form_valid(self, form):
        """Executes the task"""
        app_command = form.cleaned_data['app_command']
        command_args = form.cleaned_data['args']
        command_kwargs = form.cleaned_data['kwargs']
        if not self.is_command_valid(app_command, app_name=form.app_name):
            raise PermissionDenied  # Can not execute this command.
        task = command_exec.delay(app_command, *command_args, **command_kwargs)
        return JsonResponse({
            'task': {
                'id': task.id,
                'command': {
                    'name': app_command
                }
            }
        })


class TaskFormStatus(View):

    def get(self, request, **kwargs):
        """Reports task status"""
        task_id = str(kwargs.get("task_id"))
        async_result = AsyncResult(id=task_id, app=current_app)
        data = {
            'task': {
                'id': async_result.id,
                'ready': async_result.ready(),
            }
        }
        if async_result.failed():
            data['task']['failed'] = True
            data['task']['traceback'] = async_result.traceback
        else:
            data['task']['failed'] = False
            data['task']['output'] = async_result.result
        return JsonResponse(data)

    def post(self, request, **kwargs):
        task_id = kwargs.get('task_id')
        try:
            revoke(task_id, terminate=True)
            data = {"status": True}
        except Exception as err:
            data = {"status": False, "error": str(err)}
        return JsonResponse(data)
