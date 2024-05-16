from rest_framework.routers import DefaultRouter, DynamicRoute, Route


class SingletonRouter(DefaultRouter):
    """
    A Router for ViewSets that only have a single instance.

    This router is used for ViewSets that only have a single instance.
    It is used to generate the URLs for the ViewSet. It is used in place
    of the DefaultRouter.
    The viewset that use this router must have a `get_object` method.
    this method is used to get the object that is being operated on with out
    using pk or id or any other lookup field.

    Usage:
    ```python
    class MyViewSet(viewsets.ViewSet):
        def get_object(self):
            return self.request.user
    ```

    This router will generate the following URLs:
    ```
    GET /my-view-set/
    PATCH /my-view-set/
    PUT /my-view-set/
    DELETE /my-view-set/
    ```
    And has support for `@action` methods.

    Usage:
    ```python
    class MyViewSet(viewsets.ViewSet):
        @action(detail=False)
        def my_action(self, request, pk=None):
            pass
    ```
    This router will generate the following URLs:
    ```
    GET /my-view-set/my-action/
    ```

    """

    routes = [
        # Detail route.
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            },
            name="{basename}",
            detail=False,
            initkwargs={},
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r"^{prefix}/{url_path}{trailing_slash}$",
            name="{basename}-{url_name}",
            detail=False,
            initkwargs={},
        ),
    ]
