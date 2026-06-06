from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: Optional[int]
    quantity: int
    unit_price: Optional[Decimal]
    item_name: Optional[str] = None

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    customer_id: Optional[int]
    table_id: Optional[int]
    status: str
    total_amount: Optional[Decimal]
    created_at: datetime
    updated_at: datetime
    customer_name: Optional[str] = None
    table_number: Optional[str] = None
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str


class OrderFilters(BaseModel):
    status: Optional[str] = None
    table_id: Optional[int] = None
    customer_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int
    unit_price: float


class OrderCreate(BaseModel):
    customer_id: Optional[int] = None
    table_id: Optional[int] = None
    items: List[OrderItemCreate]