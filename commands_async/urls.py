# coding=utf-8
from django.conf.urls import url, include
from . import views

__author__ = 'alex'


cmd_patterns = ([
    url(r'^$', views.TaskFormView.as_view(), name='index'),
], 'cmd-async')

urlpatterns = [
    url(r'^cmd-async/', include(cmd_patterns)),
]