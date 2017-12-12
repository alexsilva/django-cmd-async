# coding=utf-8
from django.conf.urls import url, include
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from . import views

__author__ = 'alex'


cmd_patterns = ([
    url(r'^$', login_required(never_cache(views.TaskFormView.as_view())),
        name='index'),
    url(r'^status/(?P<task_id>.*)', login_required(never_cache(views.TaskFormStatus.as_view())),
        name='status')
], 'cmd-async')

urlpatterns = [
    url(r'^cmd-async/', include(cmd_patterns)),
]