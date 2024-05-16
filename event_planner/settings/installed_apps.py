"""
INSTALLED_APPS.

Default: [] (Empty list).

A list of strings designating all applications
that are enabled in this Django installation.

Each string should be a dotted Python path to:

- An application configuration class (preferred)
- A package containing an application.

Your code should never access INSTALLED_APPS directly. Use django.apps.apps instead.

See:

- https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
- https://docs.djangoproject.com/en/dev/ref/applications/
"""

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "corsheaders",
    "django_filters",
    "rest_framework",
    "dj_rest_auth",
    "rest_framework.authtoken",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "event_planner.api",
]
