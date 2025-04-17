from pydantic import BaseModel, Field
from typing import Optional
from pydantic.class_validators import root_validator

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_offer: Optional[bool] = None
    rating: Optional[float] = Field(None, ge=0, le=5)  # Rating should be between 0 and 5
    tags: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)  # Stock quantity should not be negative
    category_id: int  # Category ID (foreign key)

    # Root Validator to ensure rating and stock_quantity are properly validated
    @root_validator(pre=True)
    def check_validations(cls, values):
        rating = values.get('rating')
        stock_quantity = values.get('stock_quantity')

        if rating is not None and (rating < 0 or rating > 5):
            raise ValueError('Rating must be between 0 and 5.')
        if stock_quantity is not None and stock_quantity < 0:
            raise ValueError('Stock quantity cannot be negative.')

        return values

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        orm_mode = True
