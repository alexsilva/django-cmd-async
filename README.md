# django-cmd-async
Web execution of commands asynchronously.

## DJANGO settings

### It should show a list of commands to the user. Otherwise, a text input will be displayed.
[bool] COMMANDS_ASYNC_LIST (default: False)

### Login is a required feature, because we need a url.
[str]  COMMANDS_ASYNC_LOGIN_URL  (default: settings.LOGIN_URL)

### List with commands that should be ignored. [runserver, shell, etc]. An error will be shown to the user when the command is in that list.
[list] COMMANDS_ASYNC_COMMANDS_IGNORE  (default: [])

### The user who will perform tasks must have this permission. It does not need to be configured, but if configured, the user will need to have this permission to execute commands. An error message will be shown to the user if he does not have this permission.
[str]  COMMANDS_ASYNC_PERMISSION_NAME  (default: None)

### Parameter `next` to the login url.
[str]  COMMANDS_ASYNC_REDIRECT_FIELD_NAME (default: django.contrib.auth.REDIRECT_FIELD_NAME)


## App configure

#### Add the app to INSTALLED_APPS
INSTALLED_APPS.append("commands_async")

#### Include app urls
urlpatterns.append(url(r"^/app/", include('commands_async.urls')))

## Test (python manage.py runserver 8080)
In browser: http://localhost:8080/app/commands/async
