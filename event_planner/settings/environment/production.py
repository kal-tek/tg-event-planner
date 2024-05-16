# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

import os

from split_settings.tools import include

DEBUG = False

ENABLE_ADMIN = False

ENABLE_SPECTACULAR = False

CORS_ALLOWED_ORIGINS = os.environ["CORS_ALLOWED_ORIGINS"].split(",")

include("hosted.py")
