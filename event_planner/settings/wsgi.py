"""
WSGI_APPLICATION.

Default: None.

The full Python path of the WSGI application object that Django`s built-in servers
(e.g. runserver) will use.

The django-admin startproject management command will create a standard wsgi.py file
with an application callable in it, and point this setting to that application.

If not set, the return value of django.core.wsgi.get_wsgi_application() will be used.
In this case, the behavior of runserver will be identical to previous Django versions.
"""

# You should not need to change this value.
WSGI_APPLICATION = "event_planner.wsgi.application"
