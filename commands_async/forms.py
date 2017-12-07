from django import forms


class TaskForm(forms.Form):
    """ Form that displays the task list """

    app_command = forms.CharField(max_length=255, required=True)
