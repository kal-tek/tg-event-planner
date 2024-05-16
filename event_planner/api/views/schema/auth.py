from collections.abc import Mapping
from typing import Any

from drf_spectacular.utils import OpenApiExample

from ...serializers import JWTSerializerWithExpiration

token: Mapping[str, Any] = {
    "responses": {200: JWTSerializerWithExpiration},
    "examples": [
        OpenApiExample(
            "Successful Authentication",
            value={
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "user": {
                    "id": 13,
                    "email": "user@example.com",
                    "first_name": "user",
                    "last_name": "user",
                    "is_active": True,
                    "last_login": "2023-12-18T13:14:51.267172Z",
                    "date_joined": "2023-12-18T12:55:02.939768Z",
                },
                "access_expiration": "2023-12-25T13:14:51.299103Z",
                "refresh_expiration": "2023-12-27T13:14:51.299105Z",
            },
            response_only=True,
        ),
    ],
}
