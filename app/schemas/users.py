from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any

class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    WAITER = "waiter"
    COOK = "cook"
    CUSTOMER = "customer"

# Auth schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    
    class Config:
        from_attributes = True

class UserRegister(UserBase):
    password: str
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
# User management schemas
class UserRead(UserBase):
    id: int
    role: UserRole
    created_at: datetime


# CREATE
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: UserRole
    phone: Optional[str] = None
    meta: Dict[str, Any] = {}

# UPDATE (PATCH)
# All fields optional
class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None 