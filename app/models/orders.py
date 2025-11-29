from sqlalchemy import Column, BigInteger, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base, OrderStatusEnum

class Order(Base):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True)
    table_id = Column(BigInteger, ForeignKey("tables.id", ondelete="RESTRICT"), nullable=False)
    waiter_id = Column(BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    status = Column(OrderStatusEnum, nullable=False, server_default="created")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    total = Column(Numeric(12,2), nullable=False, server_default="0")

    table = relationship("Table", back_populates="orders")
    waiter = relationship("User", back_populates="waiter_orders")
    items = relationship("OrderItem", back_populates="order")