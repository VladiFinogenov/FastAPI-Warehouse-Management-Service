class ProductNotFound(Exception):
    def __init__(self):
        self.message = f"Product not found"
        super().__init__(self.message)

class InsufficientQuantity(Exception):
    def __init__(self):
        self.message = "Недостаточно товара на складе"
        super().__init__(self.message)