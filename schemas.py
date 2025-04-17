from pydantic import BaseModel, Field, field_validator
from typing import Optional

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True  # Updated for Pydantic v2

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_offer: Optional[bool] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    tags: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    category_id: int

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, rating):
        if rating is not None and (rating < 0 or rating > 5):
            raise ValueError("Rating must be between 0 and 5.")
        return rating

    @field_validator("stock_quantity")
    @classmethod
    def validate_stock(cls, stock_quantity):
        if stock_quantity is not None and stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        return stock_quantity

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True  # Updated for Pydantic v2
