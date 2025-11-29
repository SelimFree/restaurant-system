from sqlalchemy import Column, Integer, String, JSON, Enum
from db.database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    WAITER = "waiter"
    KITCHEN = "kitchen"
    CUSTOMER = "customer"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    role = Column(Enum(UserRole, name="user_roles", native_enum=False), nullable=False)
    hashed_password = Column(String, nullable=False)
    meta = Column(JSON, nullable=True)