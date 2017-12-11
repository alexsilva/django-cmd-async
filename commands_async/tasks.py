import StringIO

from celery import shared_task
from django.core.management import call_command
import sys


@shared_task(ignore_result=False,
             track_started=True)
def command_exec(name, *args, **kwargs):
    """ Run a Django command by name """
    stream = StringIO.StringIO()
    stream.encoding = sys.stdin.encoding  # hack
    kwargs['stdout'] = stream
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        call_command(name, *args, **kwargs)
    finally:
        sys.stdout = old_stdout
    return kwargs['stdout'].getvalue()
