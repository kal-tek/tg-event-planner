from .common import BinaryRenderer


class PDFRenderer(BinaryRenderer):
    media_type = "application/pdf"
    format = "pdf"
