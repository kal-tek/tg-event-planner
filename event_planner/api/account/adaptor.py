from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailConfirmationHMAC
from django.conf import settings
from rest_framework.request import Request

from ...api.models import User
from ...common.frontend_utils import get_frontend_name, get_frontend_url


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(
        self,
        request: Request,
        emailconfirmation: EmailConfirmationHMAC,
    ) -> str:
        """
        Construct the email confirmation (activation) URL with an additional.

        parameter indicating the type of user registration.

        Args:
            request (Request): The current request context.
            emailconfirmation (EmailConfirmationHMAC): Email confirmation object.

        Returns:
            str: The constructed URL for email confirmation.

        """
        user = emailconfirmation.email_address.user
        if not isinstance(user, User):
            msg = "User is not an instance of api.User"
            raise TypeError(msg)

        front_end_url = get_frontend_url(request)
        return (
            f"{front_end_url}{settings.FRONT_END_EMAIL_CONFIRMATION_PATH}?"
            f"token={emailconfirmation.key}"
        )

    def respond_email_verification_sent(self, _request: Request, _user: Any) -> Any:
        """Return a JSON response indicating that an email verification."""
        # This is suppose to return an  HTTPRedirect but since this is an API
        # we return a JSON response instead.
        return {
            "detail": "Verification e-mail sent.",
        }

    def get_additional_email_context(self, **kwargs: Any) -> dict[str, Any]:
        """
        Get additional email context for the email confirmation.

        auth_user and current_user are to be passed as keyword arguments.

        Args:
            **kwargs (Any): Additional keyword arguments.

        Returns:
            dict: The additional email context.

        """
        return {
            "email_template_signup_prefix": "account/email/email_confirmation_signup",
        }

    def send_confirmation_mail(
        self,
        request: Request,
        emailconfirmation: EmailConfirmationHMAC,
        signup: bool,  # noqa:FBT001
    ) -> None:
        """
        Send an email to the user with the email confirmation link.

        Args:
            request (Request): The current request context.
            emailconfirmation (EmailConfirmationHMAC): Email confirmation object.
            signup (bool): Whether the email confirmation is for a new user.

        """
        user = emailconfirmation.email_address.user
        if not isinstance(user, User):
            msg = "User is not an instance of api.User"
            raise TypeError(msg)
        # If auth_user is not an instance of User, set it to None
        # This happens only on registration
        auth_user: Any = request.user
        if not isinstance(auth_user, User) and not signup:
            msg = "auth_user is not an instance of api.User"
            raise TypeError(msg)

        if signup:
            auth_user = None
        current_site = get_frontend_url(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        ctx = {
            "auth_user": auth_user,
            "user": user,
            "activate_url": activate_url,
            "current_site": {
                "domain": current_site,
                "name": get_frontend_name(request),
            },
            "key": emailconfirmation.key,
        }
        email_ctx = self.get_additional_email_context(
            auth_user=auth_user,
            current_user=user,
        )
        if signup:
            email_template = email_ctx["email_template_signup_prefix"]
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)
