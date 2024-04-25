# coding=utf-8
try:
    from django.urls import include, re_path as url
except ImportError:
    from django.conf.urls import url, include
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from . import views, settings

__author__ = 'alex'


cmd_patterns = ([
    url(r'^$', login_required(never_cache(views.TaskFormView.as_view()),
                              login_url=settings.COMMANDS_ASYNC_LOGIN_URL),
        name='index'),
    url(r'^status/(?P<task_id>.*)', never_cache(views.TaskFormStatus.as_view()),
        name='status'),
    url(r'^workers/status/$', login_required(never_cache(views.CeleryWorkerStatus.as_view())),
        name='workers'),
], 'command-async')

urlpatterns = [
    url(r'^command/async/', include(cmd_patterns)),
]