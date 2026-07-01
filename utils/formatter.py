def format_money(value):
    return f"${value:.2f}"

def normalize_name(name):
    return name.strip().title()

def normalize_name_again(name):
    return name.strip().title()

def status_label(status):
    labels = {
        "pending": "Pending",
        "paid": "Paid",
        "approved": "Approved",
        "manual_review": "Manual Review",
        "shipped": "Shipped",
        "delivered": "Delivered",
        "cancelled": "Cancelled",
    }

    return labels.get(status, "Unknown")