from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI()

# In-memory database
items_db: Dict[str, "Item"] = {}

# Pydantic model for an item
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

# ******Root route******
# @app.get("/")
# def read_root():
#     return {"message": "Hello, FastAPI!"}

# *******GET endpoint with path + query*********
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "query": q}

# ********POST endpoint to receive an Item*********
# @app.post("/items/")
# def create_item(item: Item):
#     return {
#         "name": item.name,
#         "price": item.price,
#         "is_offer": item.is_offer
#     }


# Create item
@app.post("/items/")
def create_item(item: Item):
    if item.name in items_db:
        return {"error": "Item already exists"}
    items_db[item.name] = item
    return {"message": "Item created", "item": item}


# Get all items (supports optional filtering)
@app.get("/items/")
def get_all_items(q: Optional[str] = None, price: Optional[float] = None):
    results = {}
    for name, item in items_db.items():
        # Filter logic
        if q and q.lower() not in name.lower():
            continue
        if price and item.price != price:
            continue
        results[name] = item
    return results


# Get single item by name
@app.get("/items/{name}")
def get_item(name: str):
    item = items_db.get(name)
    if item:
        return item
    return {"error": "Item not found"}


# Update item
@app.put("/items/{name}")
def update_item(name: str, updated_item: Item):
    if name not in items_db:
        return {"error": "Item not found"}
    items_db[name] = updated_item
    return {"message": "Item updated", "item": updated_item}


# Delete item
@app.delete("/items/{name}")
def delete_item(name: str):
    if name in items_db:
        del items_db[name]
        return {"message": f"Item '{name}' deleted"}
    return {"error": "Item not found"}