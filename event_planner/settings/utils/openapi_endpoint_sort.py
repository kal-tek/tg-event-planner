import importlib
from collections.abc import Callable

from rest_framework.request import Request
from rest_framework.response import Response


def openapi_endpoint_sort(
    endpoint: tuple[str, str, str, Callable[[Request], Response]],
) -> tuple[str, int]:
    """
    Sort endpoints by path and method.

    This is used to sort the endpoints in the OpenAPI schema.
    Modify the sorting_reference dictionary to change the order of the endpoints.
    For each endpoint set the value to either:
        - A string starting with a ' ' to increase its priority.
        - A string starting with a '~' to decrease the priority.

    Args:
        endpoint: A tuple containing the path, method, name and view of an endpoint.

    Returns:
        A tuple containing the path and method priority of the endpoint.

    Examples:
        >>> openapi_endpoint_sort(("/docs", "get", "docs", <function>))
        (" 0", 0)
        >>> openapi_endpoint_sort(("/api/v1/users", "get", "user-list", <function>))
        ("/api/v1/users", 0)

    """
    # Import inside the function to avoid loading,
    # drf-spectacular default settings before our own.
    # Trying to do a global import will disable all of our SPECTACULAR_SETTINGS

    drf_spectacular = importlib.import_module("drf_spectacular.plumbing")

    path, method_priority = drf_spectacular.alpha_operation_sorter(endpoint)

    # The first elements of the tuple start with a space to have priority
    # over the other endpoints as ' ' > '/'
    sorting_reference = {
        "/docs": " 0",
    }
    for path_key, endpoint_priority in sorting_reference.items():
        if path.startswith(path_key):
            return endpoint_priority, method_priority

    return path, method_priority
