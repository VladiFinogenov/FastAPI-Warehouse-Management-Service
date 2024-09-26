from sqlalchemy.ext.asyncio import AsyncSession

from app.core.backend.db import async_session_maker


async def get_db_async() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
