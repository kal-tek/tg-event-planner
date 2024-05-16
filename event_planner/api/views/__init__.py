"""Where all views reside."""

from .auth import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    UserDetailsView,
)
from .registration import (
    ConfirmEmailView,
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView,
)

__all__ = (
    "LoginView",
    "LogoutView",
    "PasswordChangeView",
    "PasswordResetView",
    "PasswordResetConfirmView",
    "UserDetailsView",
    "RegisterView",
    "VerifyEmailView",
    "ConfirmEmailView",
    "ResendEmailVerificationView",
)
