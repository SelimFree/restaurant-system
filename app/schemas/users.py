from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    WAITER = "waiter"
    COOK = "cook"
    CUSTOMER = "customer"

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str