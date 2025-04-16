from pydantic import BaseModel
from typing import Optional, List

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
    rating: Optional[float] = None
    tags: Optional[str] = None
    stock_quantity: Optional[int] = None
    category_id: int  # Category ID (foreign key)

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        orm_mode = True
