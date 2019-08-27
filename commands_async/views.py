# coding=utf-8
import collections
from celery.task.control import revoke
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.http import JsonResponse
from django.views.generic import FormView, View
from celery.result import AsyncResult
from .forms import TaskForm
from django.core.management import get_commands
from commands_async.tasks import command_exec, logger
from celery import current_app
from . import settings


class TaskFormView(FormView):
    """ Task execution form """

    template_name = "cmdasync/index.html"

    form_class = TaskForm
    success_url = '.'

    commands_skip = settings.COMMANDS_ASYNC_COMMANDS_IGNORE
    command_permission_name = settings.COMMANDS_ASYNC_PERMISSION_NAME

    def is_command_valid(self, command_name, app_name=None):
        items = [command_name]
        if app_name is not None:
            items.append(app_name + "." + command_name)

        def check_command_name(name):
            return str(name) not in self.commands_skip

        return all(map(check_command_name , items))

    def has_permission(self):
        if bool(self.command_permission_name):
            has_perm = self.request.user.has_perm(self.command_permission_name)
        else:
            has_perm = True
        return has_perm

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

        if not self.is_command_valid(app_command, app_name=form.app_name) or not self.has_permission():
            if not self.request.is_ajax():
                raise PermissionDenied  # Can not execute this command.
            else:
                return JsonResponse({
                    'form': {'errors': {'app_command': [_("not allowed to run this command")]}}
                }, status=400)
        try:
            task = command_exec.apply_async(args=(app_command,) + command_args,
                                            kwargs=command_kwargs,
                                            priority=settings.COMMANDS_ASYNC_TASK_PRIORITY)
        except:
            logger.exception('failed to execute {0!s}'.format(app_command))
            task = None
        if task is None:
            return JsonResponse({
                'form': {
                    'errors': {'app_command': [
                        _("command %(command)s failed to execute") % {'command': app_command}
                    ]}
                }
            }, status=400)
        return JsonResponse({
            'task': {
                'id': task.id,
                'command': {
                    'name': app_command
                }
            }
        })


class CeleryWorkerStatus(View):
    """Reports status of workers celery"""
    def get(self, request, **kwargs):
        data = {'status': True, 'workers': []}
        try:
            for worker in current_app.control.inspect().active():
                data['workers'].append(worker)
        except Exception as err:
            data['status'] = False
            data['message'] = str(err)
        return JsonResponse(data)


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
