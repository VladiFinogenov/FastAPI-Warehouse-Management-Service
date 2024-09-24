import factory
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import Product, Category


class CategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session = 'async_db_session'
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('word')
    slug = factory.Faker('slug')
    is_active = True
    parent_id = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Получаем сессию из kwargs
        session: AsyncSession = kwargs.pop('async_db_session', None)
        if session is None:
            raise ValueError("async_db_session is required")

        # Создаем объект модели
        obj = model_class(*args, **kwargs)
        session.add(obj)
        return obj

    # @classmethod
    # def create_multiple(cls, count, session=None, **kwargs):
    #     """Метод для создания нескольких экземпляров с указанной сессией."""
    #
    #     return [cls.create(session=session, **kwargs) for _ in range(count)]


class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = 'async_db_session'
        sqlalchemy_session_persistence = 'commit'


    name = factory.Faker('word')
    slug = factory.Faker('slug')
    description = factory.Faker('text')
    price = factory.Faker('random_int', min=1, max=100)
    image_url = factory.Faker('image_url')
    stock = factory.Faker('random_int', min=1, max=100)
    rating = factory.Faker('random_int', min=1, max=100)

    # Здесь category будет подфабрикой
    category_id = factory.SubFactory(CategoryFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Получаем сессию из kwargs
        session: AsyncSession = kwargs.pop('async_db_session', None)
        if session is None:
            raise ValueError("async_db_session is required product")

        # Создаем объект модели
        obj = model_class(*args, **kwargs)
        session.add(obj)
        return obj

    # @classmethod
    # def create_multiple(cls, count, session=None, **kwargs):
    #     """Метод для создания нескольких экземпляров с указанной сессией."""
    #
    #     return [cls.create(session=session, **kwargs) for _ in range(count)]