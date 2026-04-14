"""Notification module: simulates Slack/email notifications."""


def send_notification(data: dict) -> str:
    """Simulate sending a notification and return the message content."""
    msg = (
        f"📄 New invoice processed\n"
        f"Invoice No: {data.get('invoice_no', 'N/A')}\n"
        f"Vendor: {data.get('vendor', 'N/A')}\n"
        f"Date: {data.get('date', 'N/A')}\n"
        f"Grand Total: {data.get('grand_total', 'N/A')}\n"
        f"---\n"
        f"✅ Saved to spreadsheet | 🔔 Notification sent (simulated Slack Webhook)"
    )
    print(msg)
    return msg
