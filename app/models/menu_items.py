from sqlalchemy import Column, BigInteger, Text, Numeric, Boolean, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(BigInteger, primary_key=True)
    menu_id = Column(BigInteger, ForeignKey("menus.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text)
    price = Column(Numeric(12,2), nullable=False)
    available = Column(Boolean, nullable=False, server_default="true")
    prep_time = Column(Integer, nullable=False, server_default="0")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    menu = relationship("Menu", back_populates="items")
    modifiers = relationship("ItemModifier", back_populates="item")
    order_items = relationship("OrderItem", back_populates="menu_item")