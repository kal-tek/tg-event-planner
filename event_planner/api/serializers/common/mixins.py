import contextlib
from typing import Any

from rest_framework import fields


class ReadOnlySerializerMixin(fields.Field[Any, Any, Any, Any]):
    Meta: Any
    _declared_fields: dict[str, Any]

    def __new__(cls, *args: Any, **kwargs: Any) -> "ReadOnlySerializerMixin":
        """Set all fields to read-only."""
        # ruff: noqa: SLF001
        with contextlib.suppress(AttributeError):
            cls.Meta.read_only_fields = [
                field.name for field in cls.Meta.model._meta.get_fields()
            ]

            for field in cls._declared_fields.values():
                field._kwargs["read_only"] = True

        return super().__new__(cls, *args, **kwargs)

    def create(self, *args: Any) -> None:
        """Raise an exception indicating that this serializer is read-only."""
        raise AssertionError

    def update(self, *args: Any) -> None:
        """Raise an exception indicating that this serializer is read-only."""
        raise AssertionError
