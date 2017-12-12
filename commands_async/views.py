import collections
from celery.task.control import revoke

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

    def get_context_data(self, **kwargs):
        context = super(TaskFormView, self).get_context_data(**kwargs)

        commands = collections.OrderedDict()
        commands_all = get_commands()

        # merge
        for name in commands_all:
            items = commands.setdefault(commands_all[name], [])
            items.append(name)

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
        task = command_exec.delay(app_command, *command_args, **command_kwargs)
        return JsonResponse({
            'task': {
                'id': task.id
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
