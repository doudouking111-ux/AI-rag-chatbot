"""Storage module: append extracted results to CSV (simulates Google Sheets)."""

import os, csv

CSV_PATH = "invoices.csv"
FIELDS = ["invoice_no", "vendor", "date", "total", "tax", "grand_total"]


def save_invoice(data: dict) -> str:
    """Append one invoice record to CSV and return the file path."""
    exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({k: data.get(k, "") for k in FIELDS})
    return os.path.abspath(CSV_PATH)


def load_all() -> list[dict]:
    """Load all saved invoice records."""
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, encoding="utf-8") as f:
        return list(csv.DictReader(f))
