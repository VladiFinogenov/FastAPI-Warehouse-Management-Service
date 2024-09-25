import logging

from fastapi.responses import JSONResponse
from fastapi import status
from fastapi import HTTPException

from app.data.models.order import Order, OrderItem
from app.data.repositories.order_repository import OrderRepository
from app.data.repositories.product_repository import ProductRepository
from app.domain.schemes.order_scheme import OrderCreate, OrderDetail
from app.domain.schemes.config import OrderStatus
from app.domain.schemes.product_scheme import ProductResponse, ProductInfo

logger = logging.getLogger('my_logger')


class OrderService:
    def __init__(
            self,
            order_repository: OrderRepository,
            product_repository: ProductRepository
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository

    async def create(self, order_data: OrderCreate):
        order = Order()
        try:
            for item in order_data.items:
                product = await self.product_repository.get_by_id(item.product_id)
                if not product:
                    logger.exception(f"Product {item.product_id} not found")
                    raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

                if product.quantity < item.quantity:
                    logger.exception(f"Недостаточно товара на складе {item.product_id}")
                    raise HTTPException(status_code=400, detail="Недостаточно товара на складе")

                order_item = OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity
                )
                order.items.append(order_item)

                product.quantity -= item.quantity
                await self.product_repository.update(product)

            order.status = OrderStatus.CREATED
            await self.order_repository.create(order)

            return JSONResponse(
                content={'transaction': 'Заказ успешно создан'},
                status_code=status.HTTP_201_CREATED
            )

        except HTTPException as exc:
            raise exc
        except Exception as exc:
            logger.error(f"Error in create_order: {str(exc)}")
            await self.order_repository.create(order)
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_all(self):
        logger.info('вызов метода получения всех заказов')
        return await self.order_repository.get_all()

    async def get_by_id(self, order_id: int):
        logger.info('вызов метода получения заказа')
        order = await self.order_repository.get_by_id(order_id)
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")

        order_items = []

        for item in order.items:
            product = await self.product_repository.get_by_id(item.product_id)
            if product:
                order_items.append(ProductInfo(
                    product_id=product.id,
                    quantity=item.quantity,
                    name=product.name
                ))

        return OrderDetail(
            id=order.id,
            status=order.status,
            products=order_items
        )

    async def update_status(self, order_id: int, order_status: OrderStatus):
        logger.info('вызов метода обновления заказа')
        order = await self.order_repository.get_by_id(order_id)
        if order:
            order.status = order_status
            await self.order_repository.update(order)
        else:
            raise HTTPException(status_code=404, detail="Order not found")

    async def update_order(self, order: Order):
        await self.order_repository.update(order)
