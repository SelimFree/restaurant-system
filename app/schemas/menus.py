from pydantic import BaseModel
from typing import Optional

class MenuBase(BaseModel):
    restaurant_id: int
    name: str

class MenuCreate(MenuBase):
    pass

class MenuUpdate(BaseModel):
    name: Optional[str] = None

class MenuRead(BaseModel):
    id: int
    restaurant_id: int
    name: str

    class Config:
        orm_mode = True
