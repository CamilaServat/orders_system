class Order:
    def __init__(self, order_id, customer_id, items, country, coupon, shipping_type, status):
        self.id = order_id
        self.customer_id = customer_id
        self.items = items
        self.country = country
        self.coupon = coupon
        self.shipping_type = shipping_type
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "items": self.items,
            "country": self.country,
            "coupon": self.coupon,
            "shipping_type": self.shipping_type,
            "status": self.status
        }
