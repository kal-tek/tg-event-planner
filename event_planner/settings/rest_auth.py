import os
from datetime import timedelta

from .installed_apps import INSTALLED_APPS

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "event-planner-jwt",
    "JWT_AUTH_REFRESH_COOKIE": "event-planner-refresh-token",
    "USER_DETAILS_SERIALIZER": "event_planner.api.serializers.UserDetailsSerializer",
    "LOGIN_SERIALIZER": "event_planner.api.serializers.LoginSerializer",
    "JWT_SERIALIZER": "event_planner.api.serializers.JWTSerializer",
    "JWT_SERIALIZER_WITH_EXPIRATION": (
        "event_planner.api.serializers.JWTSerializerWithExpiration"
    ),
    "JWT_AUTH_RETURN_EXPIRATION": True,
    "JWT_AUTH_HTTPONLY": False,
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_LIFETIME", "60")),
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(os.getenv("REFRESH_TOKEN_LIFETIME", "1")),
    ),
}


TOKEN_MODEL = None

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_ADAPTER = "event_planner.api.account.adaptor.CustomAccountAdapter"

# Social Authentication
SOCIAL_ACCOUNT_ENABLED = True

if SOCIAL_ACCOUNT_ENABLED:
    SOCIAL_ACCOUNT_CALLBACK_GOOGLE = os.getenv(
        "SOCIAL_ACCOUNT_CALLBACK_GOOGLE",
        "http://localhost:8000/accounts/google/login/callback/",
    )

    INSTALLED_APPS += [
        "allauth.socialaccount",
        "allauth.socialaccount.providers.facebook",
        "allauth.socialaccount.providers.twitter",
        "allauth.socialaccount.providers.google",
        "allauth.socialaccount.providers.github",
    ]

    SOCIALACCOUNT_PROVIDERS = {
        "google": {
            "APP": {
                "client_id": os.getenv("SOCIAL_ACCOUNT_GOOGLE_CLIENT_ID"),
                "secret": os.getenv("SOCIAL_ACCOUNT_GOOGLE_SECRET"),
            },
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
