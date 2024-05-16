import json
from pathlib import Path

from django.urls import reverse
from rest_framework import status

from .. import testcases


class OpenAPITests(testcases.APITestCase):
    def setUp(self) -> None:
        """
        Set up.

        - Declare the path to where the open api schema is stored.
        """
        super().setUp()
        self.spec_path = Path(__file__).parent / "openapi_spec.json"

    def test_swagger(self) -> None:
        """Ensure we can retrieve the open api schema."""
        url = reverse("schema")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsFile(self.spec_path)

        with self.spec_path.open() as file:
            spec_data = json.load(file)

        self.assertEqual(response.data, spec_data)
