from django import forms
import ast


class TaskForm(forms.Form):
    """ Form that displays the task list """

    app_command = forms.CharField(max_length=255,
                                  required=True,
                                  widget=forms.HiddenInput())

    args = forms.CharField(max_length=1024,
                           widget=forms.HiddenInput(),
                           required=False)

    kwargs = forms.CharField(max_length=1024,
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

    def clean_args(self):
        command_args = self.cleaned_data['args']
        command_args = command_args.strip("() ")
        if isinstance(command_args, (str, unicode)):
            if not command_args.startswith("["):
                command_args = "[" + command_args
            if not command_args.endswith("]"):
                command_args = command_args + "]"
        try:
            command_args = tuple(ast.literal_eval(command_args))
        except Exception as err:
            raise forms.ValidationError(str(err))
        return command_args

    def clean_kwargs(self):
        command_kwargs = self.cleaned_data['kwargs']
        command_kwargs = command_kwargs.strip()
        if isinstance(command_kwargs, (str, unicode)):
            if not command_kwargs.startswith("{"):
                command_kwargs = "{" + command_kwargs
            if not command_kwargs.endswith("}"):
                command_kwargs = command_kwargs + "}"
        try:
            command_kwargs = ast.literal_eval(command_kwargs)
        except Exception as err:
            raise forms.ValidationError(str(err))
        return command_kwargs
