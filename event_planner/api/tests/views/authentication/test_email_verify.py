from allauth.account import models as allauth_account_models
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from .... import factories
from ... import testcases


class EmailVerifyTestcase(testcases.APITestCase):
    def setUp(self) -> None:
        """
        Set up:
            - Create unverified user.
        """
        super().setUp()
        self.unverified_user = factories.UserFactory(
            is_active=True,
            with_unverified_email=True,
        )
        self.data = {"email": self.unverified_user.email}


class EmailVerifyResendTests(EmailVerifyTestcase):
    def setUp(self) -> None:
        """
        Set up:
            - Retrieve the URL for this endpoint.
        """
        super().setUp()
        self.url = reverse("resend_email_verification")

    def test_with_unverified_user_success(self) -> None:
        """
        When:
            - An unverified user requests email verification
        Then:
            - A 200 response is returned.
        """
        self.client.force_authenticate(self.unverified_user)
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EmailVerifyTests(EmailVerifyTestcase):
    def setUp(self) -> None:
        """
        Set up:
            - Retrieve the URL for this endpoint
            - Create a mail verifier.
        """
        super().setUp()
        self.email_address = self.unverified_user.emailaddress_set.first()
        self.confirmation = allauth_account_models.EmailConfirmation.create(
            self.email_address,
        )
        self.confirmation.sent = timezone.now()
        self.confirmation.save()
        self.data = {
            "key": self.confirmation.key,
        }
        self.url = reverse("account_email_verification_sent")

    def test_verify_success(self) -> None:
        """
        When:
            - A user verifies their email
        Then:
            - A 200 response is returned.
        """
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.unverified_user.refresh_from_db()
        self.assertTrue(self.unverified_user.emailaddress_set.first().verified)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)
        self.assertIn("access_expiration", response.data)
        self.assertIn("refresh_expiration", response.data)
