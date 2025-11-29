# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from db.database import Base

# class Table(Base):
#     __tablename__ = "tables"
#     id = Column(Integer, primary_key=True, index=True)
#     restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
#     name_number = Column(String, nullable=False)
#     capacity = Column(Integer)
#     status = Column(String, default="free")

#     restaurant = relationship("Restaurant", back_populates="tables")
#     orders = relationship("Order", back_populates="table")