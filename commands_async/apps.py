# coding=utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommandsAsyncConfig(AppConfig):
    """App config"""
    name = 'commands_async'

    verbose_name = _("Asynchronous commands")

    def ready(self):
        """"""
