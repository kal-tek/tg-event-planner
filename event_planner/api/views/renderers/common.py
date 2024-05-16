from collections.abc import Mapping
from typing import Any

from rest_framework.renderers import BaseRenderer


class BinaryRenderer(BaseRenderer):
    """
    Renderer for binary content.

    Performs no modifications to the binary content when rending
    """

    charset = None
    render_style = "binary"

    def render(
        self,
        data: Any,
        _accepted_media_type: str | None = None,
        _renderer_context: Mapping[str, Any] | None = None,
    ) -> Any:
        """Return the data as is."""
        return data
