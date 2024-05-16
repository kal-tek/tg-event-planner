from typing import Any, ClassVar

import rest_framework.serializers as s
from django.db import models as m
from django.views.generic import View
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from ... import exceptions


class NoPut:
    """A mixin for viewsets that removes PUT from the list of allowed methods."""

    http_method_names: ClassVar[list[str]] = [
        http_method_name
        for http_method_name in View.http_method_names
        if http_method_name != "put"
    ]


class NoPatch:
    """A mixin for viewsets that removes PATCH from the list of allowed methods."""

    http_method_names: ClassVar[list[str]] = [
        http_method_name
        for http_method_name in View.http_method_names
        if http_method_name != "patch"
    ]


class RetrieveWithQueryParams(viewsets.GenericViewSet[m.Model]):
    """A mixin that provides a default `retrieve_with_query_params()` action."""

    def retrieve_with_query_params(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Retrieve a model instance and respond with a serialized representation.

        A method that is similar to the `retrieve()` action,
        but allows to pass query parameters to the serializer.
        """
        if self.queryset is None:
            raise exceptions.RuntimeTypeError

        self.filter_queryset(self.queryset.none())
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.query_params)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class UpdateRespondNoData(viewsets.GenericViewSet[m.Model]):
    """A mixin that provides a default `update_and_respond_without_data()` action."""

    def update_and_respond_without_data(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Update a model instance and respond with 204 No Content.

        A method that is similar to the `update()` action,
        but always responds with 204 No Content and doesn't allow partial updates.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def perform_update(serializer: s.BaseSerializer[Any]) -> None:
        """
        Perform update.

        Same method as the one provided in UpdateModelMixin.
        """
        serializer.save()
