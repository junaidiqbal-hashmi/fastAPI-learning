from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None
    category: str
    description: Optional[str] = None
    category: Optional[str] = None  # New
    rating: Optional[float] = None  # New
    tags: Optional[str] = None  # New
    stock_quantity: Optional[int] = None  # New

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        orm_mode = True
