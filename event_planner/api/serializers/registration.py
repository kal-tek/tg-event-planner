import secrets
import string
from typing import TYPE_CHECKING, Any, TypedDict

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration import serializers as registration_serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers as s
from rest_framework.request import Request

from .common.mixins import ReadOnlySerializerMixin

if TYPE_CHECKING:
    from ..account import CustomAccountAdapter

UserModel = get_user_model()


class CleanedData(TypedDict):
    email: str
    first_name: str
    last_name: str


class RegistrationSerializer(
    ReadOnlySerializerMixin,
    registration_serializers.RegisterSerializer,
):
    username = None
    first_name = s.CharField(required=True)
    last_name = s.CharField(required=True)
    password1 = None
    password2 = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the serializer with empty cleaned data."""
        super().__init__(*args, **kwargs)
        self.cleaned_data: CleanedData = {
            "email": "",
            "first_name": "",
            "last_name": "",
        }

    def validate(self, data: Any) -> Any:
        """Return data as is."""
        return data

    @property
    def password(self) -> str:
        """Generate random password with 8 characters."""
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for i in range(8))

    def get_cleaned_data(self) -> CleanedData:
        """Ensure that all fields are present."""
        default_email = self.cleaned_data["email"]
        default_first_name = self.cleaned_data["first_name"]
        default_last_name = self.cleaned_data["last_name"]

        return {
            "email": self.validated_data.get("email", default_email),
            "first_name": self.validated_data.get("first_name", default_first_name),
            "last_name": self.validated_data.get("last_name", default_last_name),
        }

    def save(self, request: Request) -> AbstractUser:
        """Save the user and send a registration email."""
        adapter: CustomAccountAdapter = get_adapter(request=request)
        user: AbstractUser = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        user.set_password(self.password)
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class VerifyEmailSerializer(
    ReadOnlySerializerMixin,
    registration_serializers.VerifyEmailSerializer,
): ...
