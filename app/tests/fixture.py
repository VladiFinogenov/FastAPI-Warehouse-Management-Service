# # ASYNC_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
# # Фикстура для настройки базы данных
# @pytest_asyncio.fixture(scope="function")
# async def setup_database():
#     # Создаем асинхронный тестовый движок
#     async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, connect_args={"timeout": 0.5})
#
#     # Создаем все таблицы в базе данных
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#     # Создаем сессию
#     async_session = async_sessionmaker(
#         async_engine, expire_on_commit=False, class_=AsyncSession
#     )
#
#     return async_session


# Установите URL для тестирования.
# @pytest_asyncio.fixture(autouse=True)
# def set_test_database_url():
#     os.environ['ASYNC_DATABASE_URL'] = "sqlite+aiosqlite:///:memory:"
#
# @pytest_asyncio.fixture(loop_scope="function")
# async def async_db_connection() -> AsyncGenerator[AsyncConnection, None]:
#     async_engine = create_async_engine(
#         os.getenv('ASYNC_DATABASE_URL'), echo=False, connect_args={"timeout": 0.5}
#     )
#
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#         # Генерируем соединение для дальнейшего использования
#         async_connection = await async_engine.connect()
#         try:
#             yield async_connection
#         finally:
#             await async_connection.close()
#
#         # Удаление таблиц теперь в ‘finally’
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#
#     await async_engine.dispose()
#
#
# async def __session_within_transaction(
#         async_db_connection: AsyncConnection,
# ) -> AsyncGenerator[AsyncSession, None]:
#     session_maker = async_sessionmaker(
#         expire_on_commit=False,
#         autocommit=False,
#         autoflush=False,
#         bind=async_db_connection,
#         class_=AsyncSession,
#     )
#     async with session_maker() as session:
#         async with async_db_connection.begin():
#             yield session
#             await session.rollback()
#
# @pytest_asyncio.fixture(loop_scope="function")
# async def async_db_session(
#     async_db_connection: AsyncConnection,
# ) -> AsyncGenerator[AsyncSession, None]:
#     async for session in __session_within_transaction(async_db_connection):
#         yield session
#
#
# # Переопределение зависимости в тестах
# @pytest_asyncio.fixture(scope="function")
# def override_get_db(async_db_session: AsyncSession) -> AsyncGenerator:
#     async def get_test_db():
#         try:
#             yield async_db_session
#         finally:
#             await async_db_session.close()
#
#     yield get_test_db


# @pytest.mark.asyncio
# async def test_create_category(override_get_db):
#     app.dependency_overrides[get_db] = override_get_db
#
#
#     update_data = {
#         "name": "Update2",
#         "parent_id": None
#     }
#
#     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
#         response = await client.post(url="/category/create", json=update_data)
#
#     assert response.status_code == 201
#     assert response.json()["transaction"] == "Successful"
#
#     # Очистите зависимости после теста
#     app.dependency_overrides.clear()