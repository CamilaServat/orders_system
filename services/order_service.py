import json
from config import (
    DATA_FILE,
    DEFAULT_TAX_BR,
    DEFAULT_TAX_US,
    DEFAULT_TAX_OTHER,
    EXPRESS_SHIPPING_BR,
    EXPRESS_SHIPPING_US,
    REGULAR_SHIPPING,
    HIGH_VALUE_LIMIT,
    MEDIUM_VALUE_LIMIT,
)

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def find_customer(data, customer_id):
    for customer in data["customers"]:
        if customer["id"] == customer_id:
            return customer
    return None

def find_order(data, order_id):
    for order in data["orders"]:
        if order["id"] == order_id:
            return order
    return None

def calculate_subtotal(order):
    total = 0
    for item in order["items"]:
        total = total + item["qty"] * item["price"]
    return total

def calculate_subtotal_again(order):
    total = 0
    for item in order["items"]:
        total = total + item["qty"] * item["price"]
    return total

def calculate_tax(order):
    subtotal = calculate_subtotal(order)
    if order["country"] == "BR":
        return subtotal * DEFAULT_TAX_BR
    elif order["country"] == "US":
        return subtotal * DEFAULT_TAX_US
    return subtotal * DEFAULT_TAX_OTHER

def calculate_discount(order, customer):
    subtotal = calculate_subtotal_again(order)
    discount = 0
    if order["coupon"] == "VIP10":
        discount = subtotal * 0.10
    elif order["coupon"] == "BLACK":
        discount = subtotal * 0.20
    elif order["coupon"] == "EMPLOYEE":
        discount = subtotal * 0.30
    elif customer and customer["segment"] == "vip":
        discount = subtotal * 0.05
    return discount

def calculate_shipping(order):
    if order["shipping_type"] == "express":
        if order["country"] == "BR":
            return EXPRESS_SHIPPING_BR
        elif order["country"] == "US":
            return EXPRESS_SHIPPING_US
        else:
            return 80
    return REGULAR_SHIPPING

def calculate_total(order, customer):
    subtotal = calculate_subtotal(order)
    tax = calculate_tax(order)
    discount = calculate_discount(order, customer)
    shipping = calculate_shipping(order)
    total = subtotal + tax + shipping - discount
    if total < 0:
        total = 0
    return total

def risk_level(total, status):
    risk = "low"
    if total > MEDIUM_VALUE_LIMIT:
        risk = "medium"
    if total > HIGH_VALUE_LIMIT:
        risk = "high"
    if status == "pending" and total > HIGH_VALUE_LIMIT:
        risk = "critical"
    return risk

def order_summary(order):
    data = load_data()
    customer = find_customer(data, order["customer_id"])
    total = calculate_total(order, customer)
    risk = risk_level(total, order["status"])
    return {
        "id": order["id"],
        "customer": customer["name"] if customer else "UNKNOWN",
        "total": total,
        "risk": risk,
        "status": order["status"],
        "country": order["country"]
    }

def approve_pending_orders():
    data = load_data()
    for order in data["orders"]:
        customer = find_customer(data, order["customer_id"])
        total = calculate_total(order, customer)
        if order["status"] == "pending":
            if total > 2500:
                order["status"] = "manual_review"
            else:
                order["status"] = "approved"
    save_data(data)

# --- TP2: Evolução - Alteração controlada de status de pedido ---------------
#
# Fluxo principal suportado por esta evolução:
#   pending -> paid -> shipped -> delivered
#   pending -> cancelled
#   paid -> cancelled
#
# "approved" e "manual_review" são estados gerados pela rotina automática
# approve_pending_orders() (já existente no sistema legado) e ficam fora do
# escopo desta evolução: não são alterados manualmente por aqui, para não
# impactar a regra de negócio já existente. Por isso aparecem como estados
# terminais (sem transições manuais) nesta máquina de estados.
ORDER_STATUS_FLOW = {
    "pending": {"paid", "cancelled"},
    "paid": {"shipped", "cancelled"},
    "shipped": {"delivered"},
    "delivered": set(),
    "cancelled": set(),
    "approved": set(),
    "manual_review": set(),
}

VALID_STATUSES = set(ORDER_STATUS_FLOW.keys())

def get_allowed_next_statuses(order_id):
    """Retorna a lista de status válidos como próximo passo para um pedido."""
    data = load_data()
    order = find_order(data, order_id)
    if order is None:
        return []
    return sorted(ORDER_STATUS_FLOW.get(order["status"], set()))

def update_order_status(order_id, new_status):
    """
    Altera o status de um pedido respeitando a sequência lógica de evolução
    (pending -> paid -> shipped -> delivered), permitindo cancelamento em
    pending ou paid, e impedindo transições inválidas.

    Retorna um dicionário com:
      - success: bool
      - message: str (mensagem clara de sucesso ou erro)
      - order: dict do pedido atualizado (apenas quando success=True)
    """
    new_status = (new_status or "").strip().lower()

    data = load_data()
    order = find_order(data, order_id)

    if order is None:
        return {
            "success": False,
            "message": f"Order {order_id} not found.",
        }

    if new_status not in VALID_STATUSES:
        return {
            "success": False,
            "message": f"Unknown status '{new_status}'. Valid statuses: {sorted(VALID_STATUSES)}.",
        }

    current_status = order["status"]
    allowed = ORDER_STATUS_FLOW.get(current_status, set())

    if new_status not in allowed:
        return {
            "success": False,
            "message": (
                f"Invalid transition for order {order_id}: "
                f"'{current_status}' -> '{new_status}'. "
                f"Allowed next status(es): {sorted(allowed) if allowed else 'none (terminal status)'}."
            ),
        }

    order["status"] = new_status
    save_data(data)

    return {
        "success": True,
        "message": f"Order {order_id} status updated: '{current_status}' -> '{new_status}'.",
        "order": order,
    }