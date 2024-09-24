from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.backend.db_depends import get_db_async
from app.data.models import Product
from app.data.repositories.product_repository import ProductRepository
from app.domain.schemas.schemas import ProductCreate, ProductResponse
from app.domain.services.product_service import ProductService


router = APIRouter(tags=['products'])



def get_product_service(db: AsyncSession = Depends(get_db_async)) -> ProductService:
    product_repository = ProductRepository(db)
    return ProductService(product_repository)


@router.post("/products", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    service: Annotated[ProductService, Depends(get_product_service)]
):
    product = Product(**product_data.model_dump())
    return await service.create_product(product)

@router.get("/products", response_model=list[ProductResponse])
async def get_all_products(
    service: Annotated[ProductService, Depends(get_product_service)]
):
    return await service.get_all_products()

@router.get("/products/{id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_product_service)]
):
    product = await service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductCreate,
    service: Annotated[ProductService, Depends(get_product_service)]
):
    product = await service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_data.model_dump().items():
        setattr(product, key, value)

    await service.update_product(product)
    return product

@router.delete("/products/{id}")
async def delete_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_product_service)]
):
    product = await service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await service.delete_product(product_id)
    return {"detail": "Product deleted"}