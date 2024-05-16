import json
from pathlib import Path

from django.urls import reverse
from rest_framework.test import APIClient


def run() -> None:
    """
    Retrieve the OpenAPI schema and save it to a json file.

    The goal is to have a json file that can be used by test_openapi.py,
    allowing us to test changes to the schema.
    The schema is retrieved from the /docs/schema endpoint.
    """
    client = APIClient()
    url = reverse("schema")

    response = client.get(url, format="json")
    spec_path = Path(__file__).parent.parent / "tests" / "views" / "openapi_spec.json"
    with spec_path.open("w") as file:
        json.dump(response.data, file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    run()
