from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True) #new
    price = Column(Float)
    is_offer = Column(Boolean, default=False)
    category = Column(String) #new