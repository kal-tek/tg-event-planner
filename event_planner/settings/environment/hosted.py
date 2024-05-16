# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SECRET_KEY = os.environ["SECRET_KEY"]

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = False  # Using SECURE_SSL_REDIRECT breaks with Azure

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_SECONDS = 1

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

CSRF_TRUSTED_ORIGINS = os.environ["CSRF_TRUSTED_ORIGINS"].split(",")

sentry_sdk.init(
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=True,
)
