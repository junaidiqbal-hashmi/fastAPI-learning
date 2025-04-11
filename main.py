from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Pydantic model for an item
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

# Root route
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# GET endpoint with path + query
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# POST endpoint to receive an Item
@app.post("/items/")
def create_item(item: Item):
    return {
        "name": item.name,
        "price": item.price,
        "is_offer": item.is_offer
    }