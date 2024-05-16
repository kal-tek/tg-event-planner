# capacity_planning_sas/api/views/viewsets/base.py (lines 1-203)
from collections.abc import Mapping, Sequence
from typing import Any, TypeVar

import rest_framework.serializers as s
from django.core import exceptions
from django.db import models as m
from django_filters import rest_framework as f
from rest_framework import viewsets

ModelTypeVar = TypeVar("ModelTypeVar", bound=m.Model)


class MultiSerializerViewSetMixin(viewsets.GenericViewSet[ModelTypeVar]):
    """
    A mixin that allows to declare different serializers for different actions.

    The viewset is expected to have an attribute 'serializer_action_classes',
    which will map the action name to serializer class, i.e.:

    class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
        serializer_class = MyDefaultSerializer
        serializer_action_classes = {
           'list': MyListSerializer,
           'my_action': MyActionSerializer,
        }

        @action
        def my_action:
            ...

    If there's no entry for that action then just fallback to the regular
    get_serializer_class lookup: self.serializer_class.


    Taken from:
    https://stackoverflow.com/a/22922156
    """

    serializer_action_classes: Mapping[str, type[s.BaseSerializer[Any]]] = {}

    def get_serializer_class(self) -> type[s.BaseSerializer[Any]]:
        """
        Resolve the serializer class.

        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value).

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class.
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class MultiFilterSetViewSetMixin(viewsets.GenericViewSet[ModelTypeVar]):
    """
    A mixin that allows to declare different filtersets for different actions.

    The viewset is expected to have an attribute 'filterset_action_classes',
    which will map the action name to the filterset class, i.e.:

    class MyViewSet(MultiFilterSetViewSetMixin, ViewSet):
        filterset_action_classes = {
           'list': MyListFilterSet,
           'my_action': MyActionFilterSet,
        }

        @action
        def my_action:
            ...

    If there's no entry for that action then just fallback to
    self.list_filterset_class.

    It also removes undesired behavior from the default FilterSet.

    Currently, if you use `required=True` in a FilterSet paramater, it will require it
    in all of the different actions, instead of just the `list` one.
    """

    filterset_action_classes: Mapping[str, type[f.FilterSet]] = {}
    list_filterset_class: type[f.FilterSet]

    @property
    def filterset_class(self) -> type[f.FilterSet] | None:
        """
        Retrieve the filterset for the current action.

        Look for filterset class in self.filterset_action_classes, which
        should be a dict mapping action name (key) to filterset class (value).

        If there's no entry for that action then just fallback to
        self.list_filterset_class.
        """
        if self.action in self.filterset_action_classes:
            return self.filterset_action_classes[self.action]
        if self.action == "list":
            return self.list_filterset_class

        return None


class MultiQuerySetViewSetMixin(viewsets.GenericViewSet[ModelTypeVar]):
    """
    A mixin that allows to declare different querysets for different actions.

    The viewset is expected to have an attribute 'queryset_action_instances',
    which will map the action name to the queryset class, i.e.:

    class MyViewSet(MultiQuerySetViewSetMixin, ViewSet):
        queryset_action_instances = {
           'list': MyListQuerySet.objects.all(),
           'my_action': MyActionQuerySet.objects.all(),
        }

        @action
        def my_action:
            ...

    If there's no entry for that action then just fallback to
    self.queryset.
    """

    queryset_action_instances: Mapping[str, m.QuerySet[Any]] = {}

    def get_queryset(self) -> m.QuerySet[Any]:
        """
        Retrieve the queryset for the current action.

        Look for queryset in self.queryset_action_instances, which
        should be a dict mapping action name (key) to queryset instance (value).

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class.
        """
        try:
            queryset = self.queryset_action_instances[self.action]
            if not isinstance(queryset, m.QuerySet):
                raise exceptions.ImproperlyConfigured
            queryset = queryset.all()
        except (KeyError, AttributeError):
            return super().get_queryset()

        return queryset


class MultiPermissionClassViewSetMixin(viewsets.GenericViewSet[ModelTypeVar]):
    """
    A mixin that allows to declare different permission classes for different actions.

    The viewset is expected to have an attribute 'permission_action_classes',
    which will map the action name to permission class, i.e.:

    class MyViewSet(MultiPermissionClassViewSetMixin, ViewSet):
        permission_classes = [MyDefaultPermission]
        permission_action_classes = {
           'list': MyListPermission,
           'my_action': MyActionPermission,
        }

        @action
        def my_action:
            ...

    If there's no entry for that action then just fallback to the regular
    get_permission_class lookup: self.permission_classes.
    """

    permission_action_classes: Mapping[str, Any] = {}

    def get_permissions(self) -> Sequence[Any]:
        """
        Retrieve the permission for the current action.

        Look for permission class in self.permission_action_classes, which
        should be a dict mapping action name (key) to permission class (value).

        If there's no entry for that action then just fallback to the regular
        get_permission_class lookup: self.permission_classes.
        """
        try:
            return [
                permission()
                for permission in self.permission_action_classes[self.action]
            ]
        except (KeyError, AttributeError):
            return super().get_permissions()


class ViewSet(
    MultiSerializerViewSetMixin[ModelTypeVar],
    MultiFilterSetViewSetMixin[ModelTypeVar],
    MultiQuerySetViewSetMixin[ModelTypeVar],
    MultiPermissionClassViewSetMixin[ModelTypeVar],
):
    """
    A GenericViewSet that eases the set up of different functionality per action.

    Allows custom serializers, filtersets or querysets per action.
    """
