from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.data.models import Order


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, order: Order) -> None:
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)

    async def get_all(self):
        result = await self.db.execute(select(Order))
        return result.scalars().all()

    async def get_by_id(self, order_id: int):
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .filter(Order.id == order_id))
        return result.scalars().first()

    async def update(self, order: Order):
        await self.db.commit()

    async def delete(self, order_id: int):
        order = await self.get_by_id(order_id)
        if order:
            await self.db.delete(order)
            await self.db.commit()
