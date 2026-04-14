"""Core pipeline: parse file → AI extraction → storage → notification"""

import fitz
from extractor import extract_invoice
from storage import save_invoice
from notifier import send_notification


def parse_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF file."""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)


def run_pipeline(file_bytes: bytes, filename: str) -> dict:
    """Run the full pipeline and return results from each step."""
    text = parse_pdf(file_bytes)
    data = extract_invoice(text)
    csv_path = save_invoice(data)
    notification = send_notification(data)

    return {
        "raw_text": text,
        "extracted": data,
        "csv_path": csv_path,
        "notification": notification,
    }
