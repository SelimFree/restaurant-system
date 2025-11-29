from pydantic import BaseModel
from typing import Optional, List

class OrderCreate(BaseModel):
    table_id: int
    waiter_id: int

class OrderUpdate(BaseModel):
    status: Optional[str] = None

class OrderRead(BaseModel):
    id: int
    table_id: int
    waiter_id: int
    status: str
    total: float

    class Config:
        orm_mode = True


class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int
    notes: Optional[str] = None

class OrderItemRead(BaseModel):
    id: int
    item_id: int
    quantity: int
    status: str
    notes: Optional[str]

    class Config:
        orm_mode = True

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None