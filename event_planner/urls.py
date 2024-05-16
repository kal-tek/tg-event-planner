"""
URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from dj_rest_auth.jwt_auth import get_refresh_view
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView

from . import api
from .api import views
from .api.views import social

main_router = routers.DefaultRouter()

urlpatterns: api.typing.URLList = [
    path("api/", include(main_router.urls)),
]


urlpatterns = [
    # URLs that do not require a session or valid token
    path(
        "api/auth/password/reset/",
        views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "api/auth/password/reset/confirm/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("api/auth/token/", views.LoginView.as_view(), name="login"),
    # URLs that require a user to be logged in with a valid session / token.
    path("api/auth/logout/", views.LogoutView.as_view(), name="logout"),
    path("api/auth/user/", views.UserDetailsView.as_view(), name="user_details"),
    path(
        "api/auth/password/change/",
        views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "api/auth/email/verify/",
        views.VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path(
        "api/auth/email/resend/",
        views.ResendEmailVerificationView.as_view(),
        name="resend_email_verification",
    ),
    # URLs that require a user to be logged in with a valid session / token.
    path("api/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/auth/token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    # Registration
    path("api/registration/", views.RegisterView.as_view(), name="register"),
]

if settings.SOCIAL_ACCOUNT_ENABLED:
    urlpatterns += [
        # Social
        path(
            "api/auth/google/code/",
            social.GoogleLoginAuthorizationCodeView.as_view(),
            name="google_code_login",
        ),
        path(
            "api/auth/social_accounts/",
            social.SocialAccountListView.as_view(),
            name="social_account_list",
        ),
        path(
            "api/auth/social_accounts/<int:pk>/disconnect/",
            social.SocialAccountDisconnectView.as_view(),
            name="social_account_disconnect",
        ),
    ]


if settings.ENABLE_SPECTACULAR:
    # OpenAPI documentation
    urlpatterns += [
        path(
            "docs/schema/",
            SpectacularAPIView.as_view(),
            name="schema",
        ),
        path(
            "docs/swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger",
        ),
        path(
            "docs/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]


if settings.ENABLE_ADMIN:
    # Admin interface
    urlpatterns += [
        path("admin/", admin.site.urls),
    ]
