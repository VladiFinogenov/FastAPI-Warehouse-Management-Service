from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.backend.db_depends import get_db_async
from app.data.repositories.order_repository import OrderRepository
from app.data.repositories.product_repository import ProductRepository
from app.domain.services.order_service import OrderService
from app.domain.services.product_service import ProductService


def get_product_service(db: AsyncSession = Depends(get_db_async)) -> ProductService:
    product_repository = ProductRepository(db)
    return ProductService(product_repository)


def get_order_service(db: AsyncSession = Depends(get_db_async)) -> OrderService:
    order_repository = OrderRepository(db)
    product_repository = ProductRepository(db)
    return OrderService(order_repository, product_repository)
