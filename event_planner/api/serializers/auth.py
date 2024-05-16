from collections.abc import Callable
from typing import Any, TypedDict

from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth import serializers as auth_serializers
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers as s
from rest_framework.request import Request

from ...common.frontend_utils import get_frontend_url
from .common.mixins import ReadOnlySerializerMixin


class EmailOptions(TypedDict):
    url_generator: Callable[[Request, AbstractBaseUser, str], str]


def default_url_generator(
    request: Request,
    user: AbstractBaseUser,
    temp_key: str,
) -> str:
    """Change url to frontend url."""
    uid = user_pk_to_url_str(user)
    token = temp_key
    front_end_url = get_frontend_url(request)
    reset_front_end_path = str(settings.FRONT_END_PASSWORD_RESET_PATH)
    url = f"{front_end_url}{reset_front_end_path}?uid={uid}&token={token}"
    return url.replace("%3F", "?")


class PasswordResetSerializer(
    ReadOnlySerializerMixin,
    auth_serializers.PasswordResetSerializer,
):
    """A serializer for the password reset."""

    def get_email_options(self) -> EmailOptions:
        """Set default url generator."""
        return {
            "url_generator": default_url_generator,
        }


class PasswordChangeSerializer(
    ReadOnlySerializerMixin,
    auth_serializers.PasswordChangeSerializer,
):
    """A serializer for the password change."""


class UserDetailsSerializer(auth_serializers.UserDetailsSerializer):
    """A serializer for the user details."""


class LoginSerializer(ReadOnlySerializerMixin, auth_serializers.LoginSerializer[None]):
    """A serializer for the login."""

    username = None
    email = s.EmailField(required=True)


class JWTSerializer(ReadOnlySerializerMixin, auth_serializers.JWTSerializer):
    """A serializer for the JWT token."""

    @extend_schema_field(UserDetailsSerializer)
    def get_user(self, obj: Any) -> Any:
        """Get user details."""
        return super().get_user(obj)


class JWTSerializerWithExpiration(JWTSerializer):
    """Serializer for JWT authentication with expiration times."""

    access_expiration = s.DateTimeField()
    refresh_expiration = s.DateTimeField()
