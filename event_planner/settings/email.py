import os

try:
    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "flawlessworkflow@gmail.com")

    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")

    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

    EMAIL_PORT = os.getenv("EMAIL_PORT")

except KeyError:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
