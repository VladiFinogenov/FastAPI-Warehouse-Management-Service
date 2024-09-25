from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemes.order_scheme import OrderCreate, OrderDetail, OrderState
from app.domain.services.order_service import OrderService
from app.core.backend.db_depends import get_db_async
from app.data.repositories.order_repository import OrderRepository
from app.data.repositories.product_repository import ProductRepository


router = APIRouter(tags=['orders'])


def get_order_service(db: AsyncSession = Depends(get_db_async)) -> OrderService:
    order_repository = OrderRepository(db)
    product_repository = ProductRepository(db)
    return OrderService(order_repository, product_repository)


@router.post("/orders")
async def create_order(
        order_data: OrderCreate,
        service: Annotated[OrderService, Depends(get_order_service)]):

    return await service.create(order_data)


@router.get("/orders")
async def get_all_orders(service: Annotated[OrderService, Depends(get_order_service)]):
    return await service.get_all()


@router.get("/orders/{id}")
async def get_order(
        order_id: int,
        service: Annotated[OrderService, Depends(get_order_service)]):

    return await service.get_by_id(order_id)


@router.put("/orders/{id}")
async def update_order_status(
        order_id: int,
        order_data: OrderState,
        service: Annotated[OrderService, Depends(get_order_service)]):

    await service.update_status(order_id, order_data.status)
    return await service.get_by_id(order_id)
