from .common import FileResponse


class PDFResponse(FileResponse):
    MIME_TYPE = "application/pdf"
