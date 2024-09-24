from enum import Enum

from pydantic import BaseModel, conint
from typing import List
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

class OrderStatus(str, Enum):
    IN_PROGRESS = "В процессе"
    SHIPPED = "Отправлено"
    DELIVERED = "Доставлен"
    CANCELED = "Отменен"

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: conint(gt=0)

class OrderItem(OrderItemBase):
    pass

class OrderBase(BaseModel):
    status: OrderStatus

class OrderCreate(OrderBase):
    items: List[OrderItemBase] = []

    class Config:
        json_schema_extra = {
            "example": {
                "status": "В процессе",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 1
                    },
                ]
            }
        }

class Order(OrderBase):
    id: int
    created_at: datetime

class OrderResponse(OrderBase):
    id: int
    created_at: datetime