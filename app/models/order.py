# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
# from sqlalchemy.orm import relationship
# from datetime import datetime, timezone
# from db.database import Base

# class Order(Base):
#     __tablename__ = "orders"
#     id = Column(Integer, primary_key=True, index=True)
#     table_id = Column(Integer, ForeignKey("tables.id"))
#     waiter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
#     status = Column(String, default="pending")
#     total = Column(Numeric(10, 2), default=0.00)
#     created_at = Column(DateTime, default=datetime.now(timezone.utc))
#     updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

#     table = relationship("Table", back_populates="orders")