# from sqlalchemy import Column, Integer, String, JSON
# from sqlalchemy.orm import relationship
# from db.database import Base

# class Restaurant(Base):
#     __tablename__ = "restaurants"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     address = Column(String)
#     settings = Column(JSON)

#     menus = relationship("Menu", back_populates="restaurant")
#     tables = relationship("Table", back_populates="restaurant")