import os

from split_settings.tools import include

from event_planner.settings.installed_apps import INSTALLED_APPS
from event_planner.settings.middleware import MIDDLEWARE
from event_planner.settings.utils import insert_after_target
from event_planner.settings.warnings import SILENCED_SYSTEM_CHECKS

DEBUG = True

CORS_ALLOWED_ORIGIN_REGEXES = os.environ["CORS_ALLOWED_ORIGIN_REGEXES"].split(",")

INSTALLED_APPS += [
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "drf_spectacular",
    "django_extensions",
]

MIDDLEWARE = insert_after_target(
    sequence=MIDDLEWARE,
    target="django.middleware.security.SecurityMiddleware",
    new_element="whitenoise.middleware.WhiteNoiseMiddleware",
)


SILENCED_SYSTEM_CHECKS += [
    "security.W018",  # You should not have DEBUG set to True in deployment.
]

include("hosted.py")
include("../spectacular.py")
