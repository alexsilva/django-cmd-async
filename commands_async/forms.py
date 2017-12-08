from django import forms


class TaskForm(forms.Form):
    """ Form that displays the task list """

    app_command = forms.CharField(max_length=255,
                                  required=True,
                                  widget=forms.HiddenInput())

    params = forms.CharField(max_length=350,
                             widget=forms.HiddenInput(),
                             required=False)

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.app_name = None

    def clean_app_command(self):
        app_command = self.cleaned_data['app_command']
        app_command = app_command.rstrip("#")
        self.app_name, app_command = app_command.rsplit(".", 1)
        return app_command
