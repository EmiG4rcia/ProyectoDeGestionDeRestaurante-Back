from typing import Optional
from pydantic import BaseModel


class TableCreate(BaseModel):
    table_number: str


class TableUpdate(BaseModel):
    table_number: Optional[str] = None
    status: Optional[str] = None


class TableResponse(BaseModel):
    id: int
    table_number: str
    qr_token: str
    status: str

    class Config:
        from_attributes = True