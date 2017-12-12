from django.conf import settings


# Whether to display commands in list format
COMMANDS_ASYNC_LIST = getattr(settings, "COMMANDS_ASYNC_LIST", True)