import sys

import dj_database_url

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {}
DATABASES["default"] = dj_database_url.config(
    conn_max_age=600,
    default="postgres://postgres:postgres@localhost/event-planner",
)
DATABASES["default"]["OPTIONS"] = {"application_name": "event-planner"}

# We don't need a live database to check if there are pending migrations
checking_if_has_pending_migrations = {
    "makemigrations",
    "--check",
    "--dry-run",
}.issubset(set(sys.argv))
if checking_if_has_pending_migrations:  # pragma: no cover
    DATABASES = {"default": {"ENGINE": "django.db.backends.dummy"}}


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
