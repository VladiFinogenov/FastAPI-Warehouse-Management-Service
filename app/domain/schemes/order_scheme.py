from typing import List
from datetime import datetime
from pydantic import BaseModel, conint

from app.domain.schemes.config import OrderStatus
from app.domain.schemes.product_scheme import ProductInfo


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
    products: List[ProductInfo]

class OrderCreate(BaseModel):
    items: List[OrderItem]

    class Config:
        from_attributes = True

class OrderState(BaseModel):
    status: OrderStatus

    class Config:
        from_attributes = True

