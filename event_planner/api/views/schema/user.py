from collections.abc import Mapping
from typing import Any

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample

from ... import serializers

create: Mapping[str, Any] = {
    "request": serializers.RegistrationSerializer,
    "responses": {200: OpenApiTypes.OBJECT},
    "description": "Upon successful registration, send email to user",
    "examples": [
        OpenApiExample(
            "Successful registration",
            value={
                "detail": "Email is sent to provided email address.",
            },
            response_only=True,
        ),
    ],
}

verify: Mapping[str, Any] = {
    "request": serializers.VerifyEmailSerializer,
    "responses": {200: serializers.JWTSerializer},
    "description": "Upon success full verification, return jwt",
    "examples": [
        OpenApiExample(
            "Successful verification",
            value={
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh": "",
                "user": {
                    "id": 3,
                    "email": "user3@example.com",
                    "first_name": "John",
                    "last_name": "String",
                    "is_active": True,
                    "last_login": "2023-06-01T12:16:51.140608Z",
                    "date_joined": "2023-06-01T12:16:14.479286Z",
                },
                "access_expiration": "2023-12-25T13:14:51.299103Z",
                "refresh_expiration": "2023-12-27T13:14:51.299105Z",
            },
            response_only=True,
        ),
        OpenApiExample(
            "Failed",
            value={"detail": "not found."},
            response_only=True,
        ),
    ],
}
