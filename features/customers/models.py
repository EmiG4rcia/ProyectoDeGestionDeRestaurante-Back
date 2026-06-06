from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    orders = relationship("Order", back_populates="customer")