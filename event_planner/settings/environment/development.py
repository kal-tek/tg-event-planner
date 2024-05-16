import os
from typing import Any

from split_settings.tools import include

from event_planner.settings.installed_apps import INSTALLED_APPS

DEBUG = True

SECRET_KEY = "this is not the secret key you're looking for"  # noqa: S105

INSTALLED_APPS += [
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django_extensions",
    "drf_spectacular",
]

# Allow all origins and hosts to facilitate development
CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = ["*"]

# Use ipdb for debugging
os.environ["PYTHONBREAKPOINT"] = "ipdb.set_trace"

# Settings for django-extensions
SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PRINT_SQL_TRUNCATE = None
SHELL_PLUS_SUBCLASSES_IMPORT: list[type[Any]] = []
SHELL_PLUS_IMPORTS = [
    "from django.forms.models import model_to_dict",
    "from event_planner.api import exceptions, typing",
    "from event_planner.api import models, views, serializers, factories",
]
RUNSERVER_PLUS_PRINT_SQL_TRUNCATE = None

# Settings for generating the models-graph.png, present on the repository root
GRAPH_MODELS = {
    "app_labels": ("api",),
    "disable_sort_fields": False,  # Disable = False, disables. We should open an issue
    "exclude_models": ("ModelWith*",),
    "output": "models-graph.png",
}

include("../spectacular.py")
