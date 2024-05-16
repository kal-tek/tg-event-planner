from split_settings.tools import include

from event_planner.settings.installed_apps import INSTALLED_APPS

DEBUG = True

INSTALLED_APPS += [
    "django.contrib.admin",
    "drf_spectacular",
]

SECRET_KEY = "oh no, you found the secret key"  # noqa: S105

include("../spectacular.py")
