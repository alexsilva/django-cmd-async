from django.views.generic import FormView
from .forms import TaskForm


class TaskFormView(FormView):
    """ Task execution form """

    template_name = "cmdasync/index.html"

    form_class = TaskForm
    success_url = '.'
