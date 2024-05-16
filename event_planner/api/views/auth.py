from typing import Any

from dj_rest_auth import views as auth_views
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response

from .. import serializers
from . import schema


class LoginView(auth_views.LoginView):

    @extend_schema(**schema.auth.token)
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieve token for user."""
        return super().post(request, *args, **kwargs)  # type: ignore[no-any-return]


class LogoutView(auth_views.LogoutView):
    serializer_class = None


class PasswordChangeView(auth_views.PasswordChangeView):
    pass


class PasswordResetView(auth_views.PasswordResetView):
    serializer_class = serializers.PasswordResetSerializer


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    pass


class UserDetailsView(auth_views.UserDetailsView):
    pass
