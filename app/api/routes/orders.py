from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models.order import Order
from app.domain.schemas.schemas import OrderCreate, OrderResponse
from app.domain.services.order_service import OrderService
from app.core.backend.db_depends import get_db_async
from app.data.repositories.order_repository import OrderRepository
from app.data.repositories.product_repository import ProductRepository

router = APIRouter(tags=['orders'])


def get_order_service(db: AsyncSession = Depends(get_db_async)) -> OrderService:
    order_repository = OrderRepository(db)
    product_repository = ProductRepository(db)
    return OrderService(order_repository, product_repository)


@router.post("/orders", response_model=OrderResponse)
async def create_order(
        order_data: OrderCreate,
        service: Annotated[OrderService, Depends(get_order_service)]
):
    order = Order(**order_data.model_dump())
    return await service.create_order(order)

@router.get("/orders", response_model=list[OrderResponse])
async def get_all_orders(service: OrderService = Depends(get_order_service)):
    return await service.get_all_orders()

@router.get("/orders/{id}", response_model=OrderResponse)
async def get_order(order_id: int, service: OrderService = Depends(get_order_service)):
    order = await service.get_order_by_id(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{id}", response_model=OrderResponse)
async def update_order(order_id: int, order_data: OrderCreate, service: OrderService = Depends(get_order_service)):
    order = await service.get_order_by_id(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order_data.model_dump().items():
        setattr(order, key, value)

    await service.update_order(order)
    return order

@router.delete("/orders/{id}")
async def delete_order(order_id: int, service: OrderService = Depends(get_order_service)):
    order = await service.get_order_by_id(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    await service.delete_order(order_id)
    return {"detail": "Order deleted"}