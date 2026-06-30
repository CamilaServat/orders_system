class Customer:
    def __init__(self, customer_id, name, segment, region):
        self.id = customer_id
        self.name = name
        self.segment = segment
        self.region = region

    def describe(self):
        return f"{self.id} - {self.name} ({self.segment}/{self.region})"
