from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relationship: one category -> many items
    items = relationship("Item", back_populates="category")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    is_offer = Column(Boolean, default=False)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="items")

    rating = Column(Float, nullable=True)
    tags = Column(String, nullable=True)
    stock_quantity = Column(Integer, default=0)
