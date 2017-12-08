# coding=utf-8
from django.conf.urls import url, include
from django.views.decorators.cache import never_cache
from . import views

__author__ = 'alex'


cmd_patterns = ([
    url(r'^$', views.TaskFormView.as_view(), name='index'),
    url(r'^status/(?P<task_id>.*)', never_cache(views.TaskFormStatus.as_view()), name='status')
], 'cmd-async')

urlpatterns = [
    url(r'^cmd-async/', include(cmd_patterns)),
]