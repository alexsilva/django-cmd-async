from django.http import JsonResponse
from django.views.generic import FormView, View
from celery.result import AsyncResult
from .forms import TaskForm
from django.core.management import get_commands
from commands_async.tasks import command_exec
from celery import current_app


class TaskFormView(FormView):
    """ Task execution form """

    template_name = "cmdasync/index.html"

    form_class = TaskForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(TaskFormView, self).get_context_data(**kwargs)

        commands = {}
        commands_all = get_commands()

        # merge
        for name in commands_all:
            items = commands.setdefault(commands_all[name], [])
            items.append(name)

        context['commands'] = commands
        return context

    def form_valid(self, form):
        """Executes the task"""
        app_command = form.cleaned_data['app_command']
        task = command_exec.delay(app_command)
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
