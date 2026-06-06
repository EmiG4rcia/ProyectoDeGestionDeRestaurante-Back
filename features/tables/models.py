from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from core.database import Base


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String(10), unique=True, nullable=False)
    qr_token = Column(String(64), unique=True, nullable=False)
    status = Column(Enum("available", "occupied"), default="available")

    orders = relationship("Order", back_populates="table")