from services.order_service import load_data, order_summary, approve_pending_orders
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

def main():
    while True:
        print("1 - Print report")
        print("2 - Approve pending orders")
        print("3 - Exit")
        op = input("Choose: ")
        if op == "1":
            print_report()
        elif op == "2":
            approve_pending_orders()
            print("Approval routine executed")
        elif op == "3":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
