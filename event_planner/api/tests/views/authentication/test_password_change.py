from django.urls import reverse
from rest_framework import status

from ... import testcases


class PasswordChangeTestCase(testcases.APITestCase):
    def setUp(self) -> None:
        """
        Set up.

        - Retrieve the URL for this endpoint.
        """
        super().setUp()
        self.url = reverse("password_change")

    def test_with_success(self) -> None:
        """
        Test the successful password change of a user.

        When:
            - A client is logged in as normie
            - The client makes a request to change their password
        Then:
            - A 200 response is returned
            - The user's password is changed.
        """
        data = {
            "new_password1": "anewpassword1",
            "new_password2": "anewpassword1",
        }
        self.client.force_authenticate(self.normie)
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.client.login(email=self.normie.email, password=data["new_password1"]),
        )

    def test_with_passwords_dont_match(self) -> None:
        """
        Test the failed password change of a user with passwords that don't match.

        When:
            - A client is logged in as normie
            - The client makes a request to change their password
            - The new passwords don't match
        Then:
            - A 400 response is returned
            - The user's password is not changed.
        """
        data = {
            "new_password1": "anewpassword1",
            "new_password2": "anewpassword2",
        }
        self.client.force_authenticate(self.normie)
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            self.client.login(email=self.normie.email, password=data["new_password1"]),
        )

    def test_with_password_too_short(self) -> None:
        """
        Test the failed password change of a user with a password that is too short.

        When:
            - A client is logged in as normie
            - The client makes a request to change their password
            - The new password is too short
        Then:
            - A 400 response is returned
            - The user's password is not changed.
        """
        data = {
            "new_password1": "a",
            "new_password2": "a",
        }
        self.client.force_authenticate(self.normie)
        response = self.client.post(self.url, data=data, format="json")
        # password too short code is invalid
        # password too common code is invalid
        self.assertErrorCodes(
            response.data,
            {
                "new_password2": ["invalid", "invalid"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            self.client.login(email=self.normie.email, password=data["new_password1"]),
        )

    def test_with_not_authenticated(self) -> None:
        """
        Test the failed password change of a user when not authenticated.

        When:
            - A client is not logged in
            - The client makes a request to change their password
        Then:
            - A 401 response is returned
            - The user's password is not changed.
        """
        data = {
            "new_password1": "anewpassword1",
            "new_password2": "anewpassword1",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(
            self.client.login(email=self.normie.email, password=data["new_password1"]),
        )
