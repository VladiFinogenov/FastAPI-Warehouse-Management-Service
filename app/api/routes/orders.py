from typing import Annotated

from fastapi import APIRouter, Depends

from app.domain.schemes.order_scheme import OrderCreate, OrderState
from app.domain.services.order_service import OrderService
from app.factories import get_order_service

router = APIRouter(tags=['orders'])


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
