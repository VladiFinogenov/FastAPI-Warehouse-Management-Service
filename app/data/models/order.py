from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, event
from sqlalchemy.orm import relationship

from app.core.backend.db import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, index=True)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
