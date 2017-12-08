import cStringIO

from celery import shared_task
from django.core.management import call_command


@shared_task(ignore_result=False,
             track_started=True)
def command_exec(name, *args, **kwargs):
    """ Run a Django command by name """
    kwargs['stdout'] = cStringIO.StringIO()
    call_command(name, *args, **kwargs)
    return kwargs['stdout'].getvalue()
