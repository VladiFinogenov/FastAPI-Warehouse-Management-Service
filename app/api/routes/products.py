from typing import Annotated

from fastapi import APIRouter, Depends

from app.domain.schemes.product_scheme import (ProductCreate, ProductResponse,
                                               ProductUpdate)
from app.domain.services.product_service import ProductService
from app.factories import get_product_service

router = APIRouter(tags=['products'])


@router.post("/products")
async def create_product(
        product_data: ProductCreate,
        service: Annotated[ProductService, Depends(get_product_service)]):

    return await service.create(product_data)


@router.get("/products", response_model=list[ProductResponse])
async def get_all_products(service: Annotated[ProductService, Depends(get_product_service)]):
    return await service.get_all()


@router.get("/products/{id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_product_service)]):

    return await service.get_by_id(product_id)

# TODO перенести логику в сервис
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
    return await service.delete(product_id)
