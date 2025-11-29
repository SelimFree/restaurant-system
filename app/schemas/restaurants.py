from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class RestaurantBase(BaseModel):
    name: str
    address: Optional[str] = None
    settings: Dict[str, Any] = {}
    
    class Config:
        # Pydantic's configuration to work with SQLAlchemy models
        from_attributes = True

class RestaurantRead(RestaurantBase):
    id: int
    created_at: datetime
    # Note: We usually omit related objects (staff, tables, menus) 
    # from a basic 'read all' schema to avoid huge response payloads.