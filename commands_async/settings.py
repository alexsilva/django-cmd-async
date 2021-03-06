# coding=utf-8
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME

COMMANDS_ASYNC_TASK_OPTIONS = dict(
    expires=60 * 30,  # 30 min
    retries=0
)
COMMANDS_ASYNC_TASK_OPTIONS.update(getattr(settings, 'COMMANDS_ASYNC_TASK_OPTIONS', {}))
COMMANDS_ASYNC_TASK_PRIORITY = COMMANDS_ASYNC_TASK_OPTIONS.pop('priority', 0)

# Whether to display commands in list format
COMMANDS_ASYNC_LIST = getattr(settings, "COMMANDS_ASYNC_LIST", False)
COMMANDS_ASYNC_LOGIN_URL = getattr(settings, "COMMANDS_ASYNC_LOGIN_URL", settings.LOGIN_URL)
COMMANDS_ASYNC_COMMANDS_IGNORE = getattr(settings, "COMMANDS_ASYNC_COMMANDS_IGNORE", [])
COMMANDS_ASYNC_PERMISSION_NAME = getattr(settings, "COMMANDS_ASYNC_PERMISSION_NAME", None)
COMMANDS_ASYNC_REDIRECT_FIELD_NAME = REDIRECT_FIELD_NAME
COMMANDS_ASYNC_WORKERS_STATUS_CHECK = getattr(settings, 'COMMANDS_ASYNC_WORKERS_STATUS_CHECK', False)

