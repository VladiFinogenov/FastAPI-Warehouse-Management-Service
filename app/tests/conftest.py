from typing import AsyncGenerator

import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncConnection

from httpx import ASGITransport, AsyncClient

from app.main import app
from app.core.backend.db_depends import get_db_async
from app.core.backend.db import Base


ASYNC_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope='module')
async def async_db_connection() -> AsyncGenerator[AsyncConnection, None]:
    async_engine = create_async_engine(
        ASYNC_DATABASE_URL, echo=False, connect_args={"timeout": 0.5}
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        async_connection = await async_engine.connect()

        try:
            yield async_connection
        finally:
            await async_connection.close()

    await async_engine.dispose()


@pytest_asyncio.fixture(scope='module')
async def async_db_session(async_db_connection: AsyncConnection) -> AsyncGenerator[AsyncSession, None]:
    session_maker = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_connection,
        class_=AsyncSession,
    )
    async with session_maker() as session:
        async with async_db_connection.begin():
            yield session
            await session.rollback()


@pytest_asyncio.fixture(scope='module', autouse=True)
async def client(async_db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:

    app.dependency_overrides[get_db_async] = lambda: async_db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


# @pytest_asyncio.fixture(scope='module')
# async def create_product(async_db_session):
#     for product in MOCK_PRODUCT_DATA:
#         async_db_session.add(ProductFactory(async_db_session=async_db_session, **product))
#     await async_db_session.commit()