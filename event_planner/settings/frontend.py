"""
Frontend settings for the project.

FRONT_END_DOMAIN_URL: str = os.getenv(
    "FRONT_END_DOMAIN_URL",
    "https://example.com",
)
    The domain URL of the frontend application. This is used to construct the
    email confirmation URL and the password reset URL.

FRONT_END_PASSWORD_RESET_PATH: str = os.getenv(
    "FRONT_END_PASSWORD_RESET_PATH",
    "/authentication/password/reset/",
)
    The path for the password reset URL. This is used to construct the password
    reset URL for the email sent to the user.

FRONT_END_EMAIL_CONFIRMATION_PATH: str = os.getenv(
    "FRONT_END_EMAIL_CONFIRMATION_PATH",
    "/authentication/email/verify/",
)
    The path for the email confirmation URL. This is used to construct the email
    confirmation URL for the email sent to the user.

Usage:
    FRONT_END_DOMAIN_URL = "https://example.com"
    FRONT_END_PASSWORD_RESET_PATH = "/authentication/password/reset/"
    FRONT_END_EMAIL_CONFIRMATION_PATH = "/authentication/email/verify/"

"""

import os

FRONT_END_DOMAIN_URL = os.getenv(
    "FRONT_END_DOMAIN_URL",
    "https://example.com",
)
FRONT_END_PASSWORD_RESET_PATH = os.getenv(
    "FRONT_END_PASSWORD_RESET_PATH",
    "/authentication/password/reset/",
)

FRONT_END_EMAIL_CONFIRMATION_PATH = os.getenv(
    "FRONT_END_EMAIL_CONFIRMATION_PATH",
    "/authentication/email/verify/",
)
