from pydantic import BaseModel
from typing import Optional
from enum import Enum

class OrderStatus(Enum):
    CREATED = "created"
    SENT = "sent"
    COOKING = "cooking"
    READY = "ready"
    SERVED = "served"
    CANCELLED = "cancelled"
    
class OrderItemStatus(Enum):
    PENDING = "pending"
    COOKING = "cooking"
    READY = "ready"
    
class OrderCreate(BaseModel):
    table_id: int
    waiter_id: int
    
class OrderCreateMe(BaseModel):
    table_id: int

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderRead(BaseModel):
    id: int
    table_id: int
    waiter_id: int
    status: OrderStatus
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
    status: OrderItemStatus
    notes: Optional[str]

    class Config:
        orm_mode = True

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    status: Optional[OrderItemStatus] = None
    notes: Optional[str] = None