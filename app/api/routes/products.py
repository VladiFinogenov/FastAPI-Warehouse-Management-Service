from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.backend.db_depends import get_db_async
from app.data.models import Product
from app.data.repositories.product_repository import ProductRepository
from app.domain.services.product_service import ProductService
from app.domain.schemes.product_scheme import ProductUpdate, ProductCreate, ProductResponse

router = APIRouter(tags=['products'])



def get_product_service(db: AsyncSession = Depends(get_db_async)) -> ProductService:
    product_repository = ProductRepository(db)
    return ProductService(product_repository)


@router.post("/products", response_model=ProductResponse)
async def create_product(
        product_data: ProductCreate,
        service: Annotated[ProductService, Depends(get_product_service)]):

    product = Product(**product_data.model_dump())
    return await service.create(product)


@router.get("/products", response_model=list[ProductResponse])
async def get_all_products(service: Annotated[ProductService, Depends(get_product_service)]):
    return await service.get_all()


@router.get("/products/{id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_product_service)]):

    product = await service.get_by_id(product_id)
    return product


@router.put("/products/{id}")
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: Annotated[ProductService, Depends(get_product_service)]):

    product = await service.get_by_id(product_id)

    for key, value in product_data.model_dump().items():
        if value is not None:
            setattr(product, key, value)

    await service.update(product)
    return product


@router.delete("/products/{id}")
async def delete_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_product_service)]):

    await service.get_by_id(product_id)
    await service.delete(product_id)

    return {"detail": "Product deleted"}