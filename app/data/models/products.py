from app.core.backend.db import Base
from sqlalchemy import Column, Integer, String, Float, Boolean


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    is_active = Column(Boolean, default=True)