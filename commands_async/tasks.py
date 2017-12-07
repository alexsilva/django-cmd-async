from celery import shared_task
from django.core.management import call_command


@shared_task(ignore_result=False)
def cmdexec(name):
    """ Run a Django command by name """
    call_command(name)
