from typing import TypeAlias, TypeVar

from django.db import models as m
from django.urls import URLPattern, URLResolver

# Type Aliases
URL: TypeAlias = URLPattern | URLResolver  # pylint: disable=invalid-name
URLList: TypeAlias = list[URL]

# Type Variables
ModelTypeVar = TypeVar("ModelTypeVar", bound=m.Model)
