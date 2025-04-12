from fastapi import FastAPI, HTTPException, Path, Query, Depends, status
from pydantic import BaseModel
from typing import Optional, List
from models import Item
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal, Base

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


# Create item
@app.post("/items/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    existing_item = db.query(models.Item).filter(models.Item.name == item.name).first()
    if existing_item:
        raise HTTPException(status_code=400, detail="Item already exists")
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Get all items (with optional query filter)
@app.get("/items/", response_model=list[schemas.ItemResponse])
def get_all_items(q: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Item)
    if q:
        query = query.filter(models.Item.name.contains(q))
    return query.all()


# Get item by ID
@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Update item
@app.put("/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, updated_data: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in updated_data.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


# Delete item
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": f"Item with ID {item_id} deleted"}
