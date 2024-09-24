from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.models import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, product: Product) -> Product:
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def get_all(self):
        result = await self.db.scalars(select(Product)) # db.scalars(select(Product).where(Product.is_active == True, Product.stock > 0))
        return result.all()

    async def get_by_id(self, product_id: int):
        result = await self.db.execute(select(Product).filter(Product.id == product_id))
        return result.scalars().first()

    async def update(self, product: Product):
        await self.db.commit()

    async def delete(self, product_id: int):
        product = await self.get_by_id(product_id)
        if product:
            await self.db.delete(product)
            await self.db.commit()