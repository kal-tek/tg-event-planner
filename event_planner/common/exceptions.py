from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import set_rollback


class UnreachableError(AssertionError): ...


class RuntimeTypeError(AssertionError): ...


class ProgrammingError(AssertionError): ...


class CustomValidationError(serializers.ValidationError):
    default_detail = "Validation Message"
    default_code = "code"


class CustomAPIException(exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Custom API Message"
    default_code = "code"


class MissingQueryParameterError(CustomValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Missing query parameter"
    default_code = "missing_query_parameter"


def custom_exception_handler(exc: Exception, *args: Any, **kwargs: Any) -> Response:
    """
    Handle API exceptions in a custom way.

    Calls REST framework's default exception handler first,
    to get the standard error response.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header  # type: ignore[attr-defined]
        if getattr(exc, "wait", None):
            headers["Retry-After"] = f"{exc.wait}"  # type: ignore[attr-defined]

        if isinstance(exc.detail, list | dict):
            data = exc.get_codes()
        else:
            data = {"detail": exc.get_codes()}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return Response(
        {"detail": str(exc)},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def server_error(_request: Request, *args: Any, **kwargs: Any) -> Response:
    """Handle 500 errors."""
    data = {"detail": "Server Error (500)"}
    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
