from typing import List

from pydantic import BaseModel, conint

from app.domain.schemes.config import OrderStatus


class OrderBase(BaseModel):
    id: int

    class Config:
        from_attributes = True

class OrderItem(BaseModel):
    product_id: int
    quantity: conint(gt=0)

    class Config:
        from_attributes = True

class OrderDetail(OrderBase):
    status: str
    products: List[OrderItem]

class OrderCreate(BaseModel):
    items: List[OrderItem]

    class Config:
        from_attributes = True

class OrderState(BaseModel):
    status: OrderStatus

    class Config:
        from_attributes = True
