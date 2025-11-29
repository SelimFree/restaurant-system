from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MenuItemBase(BaseModel):
    menu_id: int
    name: str
    description: Optional[str] = None
    price: float
    available: bool = True
    prep_time: int = 0

    class Config:
        from_attributes = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    available: Optional[bool] = None
    prep_time: Optional[int] = None


class MenuItemRead(MenuItemBase):
    id: int
    created_at: datetime
