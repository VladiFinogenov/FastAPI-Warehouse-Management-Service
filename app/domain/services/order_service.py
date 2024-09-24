from fastapi import HTTPException

from app.data.models.order import Order
from app.data.repositories.order_repository import OrderRepository
from app.data.repositories.product_repository import ProductRepository


class OrderService:
    def __init__(self, order_repository: OrderRepository, product_repository: ProductRepository):
        self.order_repository = order_repository
        self.product_repository = product_repository

    async def create_order(self, order_data: Order) -> Order:

        for item in order_data.items:
            product = await self.product_repository.get_by_id(item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            if product.quantity < item.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for product {item.product_id}")

            product.quantity -= item.quantity
            await self.product_repository.update(product)

        return await self.order_repository.create(order_data)

    async def get_all_orders(self):
        return await self.order_repository.get_all()

    async def get_order_by_id(self, order_id: int):
        return await self.order_repository.get_by_id(order_id)

    async def update_order_status(self, order: Order):
        await self.order_repository.update(order)
