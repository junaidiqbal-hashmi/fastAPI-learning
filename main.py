from fastapi import FastAPI, HTTPException, Path, Query, Depends, status
from sqlalchemy.orm import Session
from models import Item, Category
import models, schemas
from database import SessionLocal, engine
from typing import List

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency: get db session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new category
@app.post("/categories/", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = models.Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Get all categories
@app.get("/categories/", response_model=List[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories

# Get a category by ID
@app.get("/categories/{category_id}", response_model=schemas.CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Create a new item
@app.post("/items/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.name == item.name).first()
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists")
    new_item = models.Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# Get all items
@app.get("/items/", response_model=List[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items

# Get item by ID
@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Get items by category
@app.get("/items/category/{category_name}", response_model=List[schemas.ItemResponse])
def get_items_by_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.name == category_name).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    items = db.query(models.Item).filter(models.Item.category_id == category.id).all()
    return items
