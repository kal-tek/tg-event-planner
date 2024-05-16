from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "event_planner.api"

    # pylint: disable=import-outside-toplevel
    def ready(self) -> None:
        """
        Set up the app.

        - Imports views and typing so we can use api.views and api.typing in urls.py.
        - Let django-stubs-ext monkeypatch some classes to add generic type support.
        """
        import django_stubs_ext
        from rest_framework import fields, generics

        django_stubs_ext.monkeypatch(
            extra_classes=(
                fields.Field,
                generics.GenericAPIView,
            ),
        )

        # pylint: disable=unused-import
        # ruff: noqa: F401
        from . import typing, views
