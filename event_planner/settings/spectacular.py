"""
Spectacular settings.

You can find more information about this file in the Spectacular documentation [0]
There you can also find the full list of settings and their values. [1]

[0] https://drf-spectacular.readthedocs.io/en/latest/settings.html
"""

import os

from event_planner.settings.utils import openapi_endpoint_sort

SERVERS = [
    {"url": "http://localhost:8000", "description": "Local development server"},
]
if os.environ.get("ALLOWED_HOSTS"):
    SERVERS.append(
        {
            "url": f"https://{os.environ['ALLOWED_HOSTS'].split(',')[0]}",
            "description": "Current server",
        },
    )

SPECTACULAR_SETTINGS = {
    "TITLE": "UeventUplanner API",
    "DESCRIPTION": "Documentation for the API",
    "VERSION": "v2023.12.21",
    "SORT_OPERATIONS": openapi_endpoint_sort,
    "SCHEMA_PATH_PREFIX": r"/api",
    "SORT_OPERATION_PARAMETERS": False,
    "ENUM_NAME_OVERRIDES": {},
    "SERVERS": SERVERS,
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
}

ENABLE_SPECTACULAR = True
