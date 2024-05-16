from typing import Any

from rest_framework.response import Response


class FileResponse(Response):
    """DRF Response to render data as a file."""

    MIME_TYPE: str

    def __init__(self, file: bytes, filename: str, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the response.

        Args:
            file: The file to render.
            filename: The name of the file.
            args: Additional arguments to pass to the Response constructor.
            kwargs: Additional keyword arguments to pass to the Response constructor.

        """
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(len(file)),
        }

        kwargs["data"] = file
        kwargs["content_type"] = self.MIME_TYPE
        kwargs["headers"] = headers
        super().__init__(*args, **kwargs)
