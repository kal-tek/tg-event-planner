from typing import Any

from django.conf import settings
from rest_framework.request import Request


def get_frontend_url(request: Request, *args: Any, **kwargs: Any) -> str:
    """
    Get frontend url based on the current setting.

    Args:
        request (Request): The current request context.
        *args (Any): Additional positional arguments.
        **kwargs (Any): Additional keyword arguments.

    Returns:
        str: The constructed URL for the frontend domain based on the current setting
        and the request context.

    Example:
        >>> get_frontend_url(request)
        "https://example.com"

    """
    front_end_url = str(settings.FRONT_END_DOMAIN_URL).rstrip("/")
    if not front_end_url:
        front_end_url = str(request.META.get("HTTP_ORIGIN", "")).rstrip("/")

    return f"{front_end_url}"


def get_frontend_name(request: Request) -> str:
    """
    Get the name of the frontend application.

    Returns:
        str: The name of the frontend application.

    Example:
        >>> get_frontend_name()
        "Example App"

    """
    front_end_url = get_frontend_url(request)
    return front_end_url.split("//")[-1].split(".")[0].capitalize()
