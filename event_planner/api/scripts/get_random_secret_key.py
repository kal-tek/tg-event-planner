from django.core.management.utils import get_random_secret_key


def run() -> None:
    """
    Retrieve a random secret key, that can be used in settings.py.

    This is useful when setting up a new project or environment.
    """
    print(get_random_secret_key())  # noqa: T201
