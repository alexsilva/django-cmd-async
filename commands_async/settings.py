# coding=utf-8
from django.conf import settings


# Whether to display commands in list format
COMMANDS_ASYNC_LIST = getattr(settings, "COMMANDS_ASYNC_LIST", True)
COMMANDS_ASYNC_LOGIN_URL = getattr(settings, "COMMANDS_ASYNC_LOGIN_URL", settings.LOGIN_URL)
COMMANDS_ASYNC_COMMANDS_IGNORE = getattr(settings, "COMMANDS_ASYNC_COMMANDS_IGNORE", [])
