"""PDF text extraction."""

import fitz


def parse_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF file."""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)
