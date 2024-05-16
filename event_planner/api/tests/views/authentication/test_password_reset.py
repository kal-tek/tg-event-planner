import re

from django.conf import settings
from django.core import mail
from django.urls import reverse
from rest_framework import status

from ....models import User
from ... import testcases


class PasswordResetTestCase(testcases.APITestCase):
    def setUp(self) -> None:
        """
        Set up.

        - Retrieve the URL for this endpoint.
        """
        super().setUp()
        self.url = reverse("password_reset")

    def test_with_success_email(self) -> None:
        """
        Test the successful password reset of a user.

        When:
            - A user requests a password reset
        Then:
            - A 200 response is returned
            - The response contains a success message
            - An email is sent to the user.
        """
        data = {"email": self.normie.email}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(
            {"detail": "Password reset e-mail has been sent."},
            response.data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(mail.outbox), 1)

    def test_with_email_not_found(self) -> None:
        """
        Test the failed password reset of a user with an email that doesn't exist.

        When:
            - A user requests a password reset
            - The email doesn't exist
        Then:
            - A 200 response is returned
            - The response contains a success message
            - No email is sent to the user.
        """
        data = {"email": "email@doesnt.exist"}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(
            {"detail": "Password reset e-mail has been sent."},
            response.data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(mail.outbox), 0)


class PasswordResetLinkTestCase(testcases.APITestCase):
    def setUp(self) -> None:
        """
        Set up.

        - Retrieve the URL for this endpoint.
        """
        super().setUp()
        self.url = reverse("password_reset")
        self.client.force_authenticate(self.superuser)
        self.front_end_password_reset_url = settings.FRONT_END_PASSWORD_RESET_PATH
        self.urlmatch_regex = (
            r"(?P<ori>.+):\/\/(?P<front_end_url>.+)\.(?P<domain>[a-z]+)"
            r"(?P<reset_url>.+)\?uid=(?P<uidb64>.+)\&token=(?P<token>\S+)"
        )

    def test_token_and_user64(self) -> None:
        """
        Test the successful password reset of a user by an admin.

        When:
            - An admin requests a password reset for a user
        Then:
            - A 200 response is returned
            - The response contains a success message
            - An email is sent to the user.
            - The email contains a link to the front end password reset page
        """
        data = {"email": self.normie.email}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(
            {"detail": "Password reset e-mail has been sent."},
            response.data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        email = mail.outbox[0]
        urlmatch = re.search(self.urlmatch_regex, str(email.body))
        self.assertIsNotNone(urlmatch, "No URL found in sent email")

    def test_confirm_complete(self) -> None:
        """
        Test the successful password reset of a user by an admin.

        When:
            - An admin requests a password reset for a user
            - The user clicks the link in the email
        Then:
            - The link in the email is valid
            - The link in the email contains the user's id and a token
            - The user can update their password
            - The user's password is updated
        """
        data = {"email": self.normie.email}
        response = self.client.post(
            self.url,
            data=data,
            format="json",
        )
        email = mail.outbox[0]
        urlmatch = re.search(self.urlmatch_regex, str(email.body))
        self.assertIsNotNone(urlmatch, "No URL found in sent email")
        if urlmatch is None:  # Help mypy figure out that urlmatch is not None
            raise AssertionError

        self.assertEqual(
            f"{urlmatch['reset_url']}",
            self.front_end_password_reset_url,
        )
        uid = urlmatch["uidb64"]
        token = urlmatch["token"]
        self.url = reverse("password_reset_confirm")
        response = self.client.post(
            self.url,
            {
                "new_password1": "anewpassword1",
                "new_password2": "anewpassword1",
                "uid": uid,
                "token": token,
            },
        )
        self.assertEqual(response.status_code, 200)
        # Check the password has been changed
        user = User.objects.get(email=self.normie)
        self.assertTrue(user.check_password("anewpassword1"))
