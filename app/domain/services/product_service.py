import logging

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.data.models import Product
from app.data.repositories.product_repository import ProductRepository
from app.domain.schemes.product_scheme import ProductCreate

logger = logging.getLogger('my_logger')


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository


    async def create(self, product_data: ProductCreate):
        logger.info('вызов метода создания продукта')

        try:
            product = Product(**product_data.model_dump())
            await self.product_repository.create(product)

            return JSONResponse(
                content={'transaction': "Товар успешно создан"},
                status_code=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.error("Error in create_order: ", exc_info=e)
            raise HTTPException(status_code=500, detail="Internal Server Error")


    async def get_all(self):
        logger.info('вызов метода получения всех продуктов')
        return await self.product_repository.get_all()


    async def get_by_id(self, product_id: int):
        logger.info('вызов метода получения продукта по id')
        product = await self.product_repository.get_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product


    async def update(self, product: Product):
        logger.info('вызов метода обновления продукта')
        await self.product_repository.update(product)


    async def delete(self, product_id: int):
        logger.info('вызов метода удаления продукта')

        try:
            await self.product_repository.delete(product_id)
            return JSONResponse(
                content={'transaction': "Product deleted"},
                status_code=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.error("Error in create_order: ", exc_info=e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
