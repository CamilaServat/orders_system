def format_money(value):
    return f"${value:.2f}"

def normalize_name(name):
    return name.strip().title()

def normalize_name_again(name):
    return name.strip().title()

def status_label(status):
    if status == "paid":
        return "Paid"
    elif status == "pending":
        return "Pending"
    elif status == "approved":
        return "Approved"
    elif status == "manual_review":
        return "Manual Review"
    elif status == "cancelled":
        return "Cancelled"
    return "Unknown"
