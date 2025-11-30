from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class TableStatus(Enum):
    FREE = "free"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    

class TableBase(BaseModel):
    restaurant_id: int
    name_number: str
    capacity: int
    status: Optional[TableStatus] = TableStatus.FREE

    class Config:
        from_attributes = True


class TableCreate(BaseModel):
    restaurant_id: int
    name_number: str
    capacity: int
    status: Optional[TableStatus] = TableStatus.FREE


class TableUpdate(BaseModel):
    name_number: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[TableStatus] = None


class TableRead(TableBase):
    id: int
    created_at: datetime
