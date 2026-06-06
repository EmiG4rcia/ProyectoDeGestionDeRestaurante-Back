from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class MenuItemCreate(BaseModel):
    category: str
    name: str
    description: Optional[str] = None
    price: Decimal
    is_available: bool = True


class MenuItemUpdate(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    is_available: Optional[bool] = None


class MenuItemResponse(BaseModel):
    id: int
    category: Optional[str]
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]
    is_available: bool
    popularity_score: int

    class Config:
        from_attributes = True