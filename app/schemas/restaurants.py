from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class RestaurantBase(BaseModel):
    name: str
    address: Optional[str] = None
    settings: Dict[str, Any] = {}
    
    class Config:
        from_attributes = True

class RestaurantRead(RestaurantBase):
    id: int
    created_at: datetime


# CREATE
class RestaurantCreate(BaseModel):
    name: str
    address: Optional[str] = None
    settings: Dict[str, Any] = {}


# UPDATE (PATCH)
# All fields optional
class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None 