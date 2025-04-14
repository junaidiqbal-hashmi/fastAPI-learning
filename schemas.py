from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None
    category: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        orm_mode = True
