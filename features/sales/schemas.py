from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class PaymentResponse(BaseModel):
    id: int
    order_id: Optional[int]
    amount: Optional[Decimal]
    method: str
    status: str
    created_at: datetime
    customer_name: Optional[str] = None
    table_number: Optional[str] = None

    class Config:
        from_attributes = True


class PaymentStatusUpdate(BaseModel):
    status: str


class SalesSummary(BaseModel):
    total_orders: int
    total_revenue: Decimal
    pending_payments: int
    completed_payments: int
    payment_received_pending: int
    
class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    method: str = "cash"