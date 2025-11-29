from sqlalchemy import Column, BigInteger, Text, JSON, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)
    address = Column(Text)
    settings = Column(JSON, default={})
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    staff = relationship("Staff", back_populates="restaurant")
    tables = relationship("Table", back_populates="restaurant")
    menus = relationship("Menu", back_populates="restaurant")