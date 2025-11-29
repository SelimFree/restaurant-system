# from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Numeric
# from sqlalchemy.orm import relationship
# from db.database import Base

# class Menu(Base):
#     __tablename__ = "menus"
#     id = Column(Integer, primary_key=True, index=True)
#     restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
#     name = Column(String, nullable=False)

#     restaurant = relationship("Restaurant", back_populates="menus")
#     items = relationship("MenuItem", back_populates="menu")
    
    
# class MenuItem(Base):
#     __tablename__ = "menu_items"
#     id = Column(Integer, primary_key=True, index=True)
#     menu_id = Column(Integer, ForeignKey("menus.id"))
#     name = Column(String, nullable=False)
#     description = Column(String)
#     price = Column(Numeric(10, 2), nullable=False)
#     available = Column(Boolean, default=True)
#     prep_time = Column(Integer)

#     menu = relationship("Menu", back_populates="items")