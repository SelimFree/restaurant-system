from sqlalchemy import Column, BigInteger, Text, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class ItemModifier(Base):
    __tablename__ = "item_modifiers"

    id = Column(BigInteger, primary_key=True)
    item_id = Column(BigInteger, ForeignKey("menu_items.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    price_delta = Column(Numeric(12,2), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    item = relationship("MenuItem", back_populates="modifiers")