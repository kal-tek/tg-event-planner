from django.conf import settings
from django.core import mail
from django.urls import reverse
from rest_framework import status

from ....models import User
from ... import testcases


class RegistrationTestcase(testcases.APITestCase):
    def setUp(self) -> None:
        """
        Set up.

        - Retrieves the URL for this endpoint.
        """
        super().setUp()
        self.url = reverse("register")


class RegistrationSuccessTestcase(RegistrationTestcase):
    def test_success(self) -> None:
        """
        Test success.

        When:
            - A normie user registers
        Then:
            - A 201 response is returned
            - The response contains an access token
            - The response contains a refresh token
            - The response contains the user's data
            - An email is sent
            - The user is created
            - The user is active.
        """
        data = {
            "email": "register@me.com",
            "first_name": "Register",
            "last_name": "Me",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Please Confirm Your E-mail Address", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, [data["email"]])
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)

        user = User.objects.get(email=data["email"])
        self.assertTrue(user.is_active)


class RegistrationFailTestcase(RegistrationTestcase):
    def test_fail_with_existing_user(self) -> None:
        """
        Test that a user cannot register with an existing email.

        When:
            - A normie user registers
            - The user already exists
        Then:
            - A 400 response is returned
            - The response contains an error message
            - No email is sent.
        """
        data = {
            "email": self.normie.email,
            "first_name": "Register",
            "last_name": "Me",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertErrorCodes(
            response.data,
            {
                "email": {"invalid"},
            },
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_fail_with_invalid_email(self) -> None:
        """
        Test that a user cannot register with an invalid email.

        When:
            - A normie user registers
            - The email is invalid
        Then:
            - A 400 response is returned
            - The response contains an error message
            - No email is sent.
        """
        data = {
            "email": "invalid",
            "first_name": "Register",
            "last_name": "Me",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertErrorCodes(
            response.data,
            {
                "email": {"invalid"},
            },
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_fail_with_no_data(self) -> None:
        """
        Test that a user cannot register with no provided data.

        When:
            - A normie user registers
            - No data is provided
        Then:
            - A 400 response is returned
            - The response contains an error message
            - No email is sent.
        """
        response = self.client.post(self.url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertErrorCodes(
            response.data,
            {
                "email": {"required"},
                "first_name": {"required"},
                "last_name": {"required"},
            },
        )
        self.assertEqual(len(mail.outbox), 0)
