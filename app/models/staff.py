from sqlalchemy import Column, BigInteger, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Staff(Base):
    __tablename__ = "staff"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    restaurant_id = Column(BigInteger, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    role_meta = Column(JSON, default={})
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="staff_roles")
    restaurant = relationship("Restaurant", back_populates="staff")