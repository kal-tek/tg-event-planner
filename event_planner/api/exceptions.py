from rest_framework import exceptions, serializers, status


class UnreachableError(AssertionError): ...


class RuntimeTypeError(AssertionError): ...


class ProgrammingError(AssertionError): ...


class CustomValidationError(serializers.ValidationError):
    default_detail = "Message"
    default_code = "code"


class CustomAPIException(exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Message"
    default_code = "code"
