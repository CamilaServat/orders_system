from services.order_service import (
    load_data,
    order_summary,
    approve_pending_orders,
    find_order,
    update_order_status,
    get_allowed_next_statuses,
)
from services.payment_service import payment_label
from utils.formatter import format_money, status_label

def print_report():
    data = load_data()
    print("=== ORDERS REPORT ===")
    total_pending = 0
    total_value = 0
    by_country = {}

    for order in data["orders"]:
        summary = order_summary(order)
        if summary["status"] == "pending":
            total_pending += 1
        total_value += summary["total"]

        if summary["country"] not in by_country:
            by_country[summary["country"]] = 0
        by_country[summary["country"]] = by_country[summary["country"]] + 1

        print("Order:", summary["id"])
        print("Customer:", summary["customer"])
        print("Total:", format_money(summary["total"]))
        print("Risk:", summary["risk"])
        print("Status:", status_label(summary["status"]))
        print("Payment Label:", payment_label(summary["status"]))
        print("-----------------------")

    print("TOTAL PENDING:", total_pending)
    print("TOTAL VALUE:", format_money(total_value))
    print("ORDERS BY COUNTRY:", by_country)

def update_status_menu():
    """TP2: fluxo de CLI para alteracao controlada de status de um pedido."""
    raw_id = input("Enter order ID: ").strip()
    try:
        order_id = int(raw_id)
    except ValueError:
        print("Invalid order ID. Please enter a numeric ID.")
        return

    data = load_data()
    order = find_order(data, order_id)
    if order is None:
        print(f"Order {order_id} not found.")
        return

    print("Current status:", status_label(order["status"]))
    allowed = get_allowed_next_statuses(order_id)

    if not allowed:
        print("This order has no valid manual transitions (terminal or externally managed status).")
        return

    print("Allowed next status(es):", ", ".join(allowed))
    new_status = input("New status: ").strip().lower()

    result = update_order_status(order_id, new_status)
    print(result["message"])

def main():
    while True:
        print("1 - Print report")
        print("2 - Approve pending orders")
        print("3 - Update order status")
        print("4 - Exit")
        op = input("Choose: ")
        if op == "1":
            print_report()
        elif op == "2":
            approve_pending_orders()
            print("Approval routine executed")
        elif op == "3":
            update_status_menu()
        elif op == "4":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
