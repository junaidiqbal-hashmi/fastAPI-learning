from fastapi import FastAPI, HTTPException, Path, Query, Depends, status
from pydantic import BaseModel
from typing import Optional, List
from models import Item
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal, Base
from enum import Enum

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Category Enum
class CategoryEnum(str, Enum):
    books = "books"
    electronics = "electronics"
    clothing = "clothing"

# Dependency: get db session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# New route to filter by price range
@app.get("/items/filter/", response_model=list[schemas.ItemResponse])
def filter_items(
    min_price: float = Query(0, ge=0),  # Minimum price with validation
    max_price: float = Query(1000, le=10000),  # Max price with upper limit
    db: Session = Depends(get_db)
):
    query = db.query(models.Item).filter(models.Item.price >= min_price, models.Item.price <= max_price)
    return query.all()


# Create item
@app.post("/items/", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)  # ✅ status_code added
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    existing_item = db.query(models.Item).filter(models.Item.name == item.name).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Item already exists")
    db_item = models.Item(**item.dict())  # Later use model_dump()
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Get all items (with optional query filter)
@app.get("/items/", response_model=list[schemas.ItemResponse])
def get_all_items(
    q: str = Query(default=None, min_length=3, max_length=50),  #  Query validation
    db: Session = Depends(get_db)
):
    query = db.query(models.Item)
    if q:
        query = query.filter(models.Item.name.contains(q))
    return query.all()


# Path param validation + 404 handling
@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def get_item(
    item_id: int = Path(..., gt=0),  # Path validation
    db: Session = Depends(get_db)
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")  # Proper 404
    return item


# Get items by category using Enum
@app.get("/items/category/{category_name}", response_model=list[schemas.ItemResponse])
def get_items_by_category(category_name: CategoryEnum, db: Session = Depends(get_db)):
    items = db.query(models.Item).filter(models.Item.category == category_name.value).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found in this category")
    return items


# Update item with path validation + model_dump()
@app.put("/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(
    updated_data: schemas.ItemCreate, item_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in updated_data.model_dump().items():  # Use model_dump()
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


#Delete item with 204 NO CONTENT and path validation
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)  # status_code added
def delete_item(
    item_id: int = Path(..., gt=0),  # Path validation
    db: Session = Depends(get_db)
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return  # No return needed for 204
