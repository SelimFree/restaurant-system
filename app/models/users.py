from sqlalchemy import Column, BigInteger, Text, JSON, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base, UserRoleEnum

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    phone = Column(Text)
    role = Column(UserRoleEnum, nullable=False)
    hashed_password = Column(Text, nullable=False)
    meta = Column(JSON, default={})
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # relationships
    staff_roles = relationship("Staff", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    waiter_orders = relationship("Order", back_populates="waiter")