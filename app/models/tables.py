from sqlalchemy import Column, BigInteger, Text, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base, TableStatusEnum

class Table(Base):
    __tablename__ = "tables"

    id = Column(BigInteger, primary_key=True)
    restaurant_id = Column(BigInteger, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    name_number = Column(Text, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(TableStatusEnum, nullable=False, server_default="free")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    restaurant = relationship("Restaurant", back_populates="tables")
    orders = relationship("Order", back_populates="table")