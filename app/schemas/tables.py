from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TableBase(BaseModel):
    restaurant_id: int
    name_number: str
    capacity: int
    status: Optional[str] = "free"

    class Config:
        from_attributes = True


class TableCreate(BaseModel):
    restaurant_id: int
    name_number: str
    capacity: int
    status: Optional[str] = "free"


class TableUpdate(BaseModel):
    name_number: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None


class TableRead(TableBase):
    id: int
    created_at: datetime
