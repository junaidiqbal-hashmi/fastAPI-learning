from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Make sure tables exist
models.Base.metadata.create_all(bind=engine)

# Sample data
sample_items = [
    {"name": "Laptop", "description": "Powerful business laptop", "price": 1200.0, "is_offer": True, "category": "electronics"},
    {"name": "Smartphone", "description": "Flagship Android phone", "price": 799.99, "is_offer": False, "category": "electronics"},
    {"name": "T-Shirt", "description": "100% cotton", "price": 19.99, "is_offer": True, "category": "clothing"},
    {"name": "Novel", "description": "Best-selling fiction", "price": 14.99, "is_offer": False, "category": "books"},
    {"name": "Headphones", "description": "Noise-cancelling", "price": 199.99, "is_offer": True, "category": "electronics"},
    {"name": "Cookbook", "description": "Delicious recipes", "price": 24.99, "is_offer": False, "category": "books"},
]

# Create DB session
db: Session = SessionLocal()

for item_data in sample_items:
    existing = db.query(models.Item).filter(models.Item.name == item_data["name"]).first()
    if not existing:
        item = models.Item(**item_data)
        db.add(item)

db.commit()
db.close()

print("Sample data inserted!")
