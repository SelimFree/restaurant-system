# from pydantic import BaseModel
# from typing import Optional

# class MenuItemBase(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     available: bool = True

# class MenuItemCreate(MenuItemBase):
#     pass

# class MenuBase(BaseModel):
#     name: str

# class MenuCreate(MenuBase):
#     pass

# class MenuResponse(MenuBase):
#     id: int
#     items: list[MenuItemBase] = []
#     class Config:
#         orm_mode = True