from services.order_service import calculate_subtotal_again

def calculate_tax_again(order):
    subtotal = calculate_subtotal_again(order)
    if order["country"] == "BR":
        return subtotal * 0.12
    elif order["country"] == "US":
        return subtotal * 0.07
    return subtotal * 0.10

def calculate_discount_again(order, customer):
    subtotal = calculate_subtotal_again(order)
    if order["coupon"] == "VIP10":
        return subtotal * 0.10
    elif order["coupon"] == "BLACK":
        return subtotal * 0.20
    elif order["coupon"] == "EMPLOYEE":
        return subtotal * 0.30
    elif customer and customer["segment"] == "vip":
        return subtotal * 0.05
    return 0

def payment_label(status):
    if status in ["paid", "approved"]:
        return "OK"
    elif status == "pending":
        return "WAITING"
    return "CHECK"
