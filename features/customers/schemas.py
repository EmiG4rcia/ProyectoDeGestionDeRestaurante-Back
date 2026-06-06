from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CustomerCreate(BaseModel):
    phone_number: str
    name: Optional[str] = None


class CustomerUpdate(BaseModel):
    phone_number: Optional[str] = None
    name: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    phone_number: str
    name: Optional[str]
    created_at: datetime
    total_orders: Optional[int] = 0

    class Config:
        from_attributes = True


class CustomerDetailResponse(BaseModel):
    id: int
    phone_number: str
    name: Optional[str]
    created_at: datetime
    orders: list[dict] = []

    class Config:
        from_attributes = True