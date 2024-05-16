"""
Settings for Django project.

You can find more information about this file in the Django documentation [0]
There you can also find the full list of settings and their values. [1]

[0] https://docs.djangoproject.com/en/4.2/topics/settings/
[1] https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os

from split_settings.tools import include, optional

ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

base_settings = [
    "base_dir.py",
    "installed_apps.py",
    "wsgi.py",
    "urlconf.py",
    "middleware.py",
    "auth_user_model.py",
    "password.py",
    "database.py",
    "restframework.py",
    "rest_auth.py",
    "templates.py",
    "warnings.py",
    "email.py",
    "frontend.py",
    "i18n.py",
    "static.py",
    "admin.py",
    optional(f"environment/{ENVIRONMENT}.py"),
    optional("environment/local.py"),
]

# Include settings:
include(*base_settings)
