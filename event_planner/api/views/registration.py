from typing import Any

from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.registration import views as registration_views
from dj_rest_auth.utils import jwt_encode
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings as jwt_settings

from .. import serializers
from . import schema


class RegisterView(registration_views.RegisterView):
    serializer_class = serializers.RegistrationSerializer


class VerifyEmailView(registration_views.VerifyEmailView):
    """A view for verifying email."""

    @extend_schema(**schema.user.verify)
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Verify email address using the key in the URL."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs["key"] = serializer.validated_data["key"]
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        data = self.get_response_data(confirmation.email_address.user)
        return Response(data, status=status.HTTP_200_OK)

    def get_response_data(self, user: type[AbstractBaseUser]) -> Any:
        """Upon success full verification, return jwt."""
        # This will return a JWT token for the user
        # This is only called on the first verification click
        access_token, refresh_token = jwt_encode(user)
        access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
        refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
        data = {
            "user": user,
            "access": access_token,
            "refresh": refresh_token,
            "access_expiration": access_token_expiration,
            "refresh_expiration": refresh_token_expiration,
        }
        return api_settings.JWT_SERIALIZER_WITH_EXPIRATION(
            data,
            context=self.get_serializer_context(),
        ).data

    def get_serializer_context(self) -> dict[str, Any]:
        """Extra context provided to the serializer class."""
        return {"request": self.request, "format": self.format_kwarg, "view": self}


class ConfirmEmailView(registration_views.ConfirmEmailView):
    """A view for confirming email."""


class ResendEmailVerificationView(registration_views.ResendEmailVerificationView):
    """A view for resending email verification."""
