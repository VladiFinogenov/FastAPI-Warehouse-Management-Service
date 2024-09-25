import logging

from fastapi.responses import JSONResponse
from fastapi import status, HTTPException

from app.data.models.order import Order, OrderItem
from app.data.repositories.order_repository import OrderRepository
from app.data.repositories.product_repository import ProductRepository
from app.domain.schemes.order_scheme import OrderCreate, OrderDetail
from app.domain.schemes.config import OrderStatus
# from app.domain.schemes.order_scheme import OrderItem
from app.domain.exceptions import ProductNotFound, InsufficientQuantity

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
        logger.info('вызов метода создания заказа')
        order = Order()

        try:
            for item in order_data.items:
                product = await self.product_repository.get_by_id(item.product_id)
                if not product:
                    logger.exception(f"Product id: {item.product_id} not found")
                    raise ProductNotFound

                if product.quantity < item.quantity:
                    logger.exception(f"Недостаточно товара на складе {item.product_id}")
                    raise InsufficientQuantity

                order_item = OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity
                )
                order.items.append(order_item)

                product.quantity -= item.quantity
                await self.product_repository.update(product)

            order.status = OrderStatus.CREATED
            await self.order_repository.create(order)

            logger.info(f'создан заказ c id: {order.id}')
            return JSONResponse(
                content={'transaction': 'Заказ успешно создан'},
                status_code=status.HTTP_201_CREATED
            )

        except ProductNotFound as e:
            raise HTTPException(status_code=404, detail=e.message)
        except InsufficientQuantity as e:
            raise HTTPException(status_code=400, detail=e.message)
        except Exception as e:
            logger.error("Error in create_order: ", exc_info=e)
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
            order_item = OrderItem(
                product_id=item.product_id,
                quantity=item.quantity
            )
            order_items.append(order_item)

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
