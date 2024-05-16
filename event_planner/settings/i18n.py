# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

import os

LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en-us")

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
