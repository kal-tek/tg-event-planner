from django.urls import reverse
from rest_framework import status

from .... import factories
from ... import testcases


class LoginTestcase(testcases.APITestCase):
    def setUp(self) -> None:
        """
        Set up.

        - Retrieve the URL for this endpoint.
        """
        super().setUp()
        self.url = reverse("login")
        self.inactive_user = factories.UserFactory(
            is_active=False,
            with_known_password=True,
        )

    def test_with_normie_success(self) -> None:
        """
        Test the successful login of a normal user.

        When:
            - A normie user logs in
        Then:
            - A 200 response is returned
            - The response contains an access token
            - The response contains a refresh token
            - The response contains the user's data.
        """
        data = {"email": self.normie.email, "password": self.known_password}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

    def test_fail_normie_inactive(self) -> None:
        """
        Test the failed login of an inactive normal user.

        When:
            - A normie user logs in
            - The user is inactive
        Then:
            - A 400 response is returned
            - The response contains an error message.
        """
        data = {"email": self.inactive_user.email, "password": self.known_password}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertErrorCodes(
            response.data,
            {
                "non_field_errors": {"invalid"},
            },
        )

    def test_fail_with_unknown_user(self) -> None:
        """
        Test the failed login of an user with no matching email.

        When:
            - An unknown user logs in
        Then:
            - A 400 response is returned
            - The response contains an error message.
        """
        data = {"email": "unknown.user@unknowndomain.com", "password": "unknown"}
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertErrorCodes(
            response.data,
            {
                "non_field_errors": {"invalid"},
            },
        )
