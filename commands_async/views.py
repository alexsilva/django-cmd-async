from django.http import JsonResponse
from django.views.generic import FormView

from .forms import TaskForm
from django.core.management import get_commands
from .tasks import command_exec


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
            'task': task.id
        })