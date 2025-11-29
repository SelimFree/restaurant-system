from sqlalchemy import Column, BigInteger, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base, OrderItemStatusEnum

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(BigInteger, primary_key=True)
    order_id = Column(BigInteger, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(BigInteger, ForeignKey("menu_items.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(OrderItemStatusEnum, nullable=False, server_default="pending")
    notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")