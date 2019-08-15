import StringIO

from celery import shared_task
from django.core.management import call_command
import sys


class Output(object):
    encoding = 'utf-8'

    def __init__(self, stream):
        self.stream = stream
        self.stdout = sys.stdout

    def __enter__(self):
        sys.stdout = self.stream
        return self

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, 'stream'), name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.stdout

    def __str__(self):
        return self.stream.getvalue()


@shared_task(ignore_result=False,
             track_started=True)
def command_exec(name, *args, **kwargs):
    """ Run a Django command by name """
    stream = Output(StringIO.StringIO())
    try:
        with stream:
            kwargs['stdout'] = stream
            try:
                call_command(name, *args, **kwargs)
            except SystemExit as err:
                if hasattr(err, 'code') and err.code != 0:
                    raise
    finally:
        return str(stream)
