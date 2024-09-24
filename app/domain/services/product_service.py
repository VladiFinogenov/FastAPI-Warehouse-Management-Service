import logging

from app.data.models import Product
from app.data.repositories.product_repository import ProductRepository


logger = logging.getLogger('my_logger')

class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def create_product(self, product: Product) -> Product:
        logger.info('вызов метода создания продукта')
        return await self.product_repository.create(product)

    async def get_all_products(self):
        logger.info('вызов метода получения всех продуктов')
        return await self.product_repository.get_all()

    async def get_product_by_id(self, product_id: int):
        logger.info('вызов метода получения продукта по id')
        return await self.product_repository.get_by_id(product_id)

    async def update_product(self, product: Product):
        logger.info('вызов метода обновления продукта')
        await self.product_repository.update(product)

    async def delete_product(self, product_id: int):
        logger.info('вызов метода удаления продукта')
        await self.product_repository.delete(product_id)