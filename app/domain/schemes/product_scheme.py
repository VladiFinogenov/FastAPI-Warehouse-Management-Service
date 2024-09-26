from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

class ProductResponse(ProductBase):
    id: int

class ProductInfo(BaseModel):
    id: int
    quantity: int
    name: str

    class Config:
        from_attributes = True
