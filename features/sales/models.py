from sqlalchemy import Column, Integer, DECIMAL, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    amount = Column(DECIMAL(10, 2), nullable=True)
    method = Column(
        Enum("cash", "card", "qr_payment"),
        default="cash"
    )
    status = Column(
        Enum("pending", "payment_received", "completed", "failed"),
        default="pending"
    )
    created_at = Column(TIMESTAMP, server_default=func.now())

    order = relationship("Order")