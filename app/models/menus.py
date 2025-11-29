from sqlalchemy import Column, BigInteger, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Menu(Base):
    __tablename__ = "menus"

    id = Column(BigInteger, primary_key=True)
    restaurant_id = Column(BigInteger, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    restaurant = relationship("Restaurant", back_populates="menus")
    items = relationship("MenuItem", back_populates="menu")