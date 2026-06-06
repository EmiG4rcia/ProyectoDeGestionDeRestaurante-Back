from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=True)
    status = Column(
        Enum("pending", "confirmed", "preparing", "ready", "delivered", "cancelled"),
        default="pending"
    )
    total_amount = Column(DECIMAL(10, 2), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    items = relationship("OrderItem", back_populates="order")
    customer = relationship("Customer", back_populates="orders")
    table = relationship("Table", back_populates="orders")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=True)
    quantity = Column(Integer, default=1)
    unit_price = Column(DECIMAL(10, 2), nullable=True)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")