from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --------------------
# Category Tests
# --------------------

def test_create_category():
    response = client.post("/categories/", json={"name": "Electronics"})
    assert response.status_code == 200
    assert response.json()["name"] == "Electronics"

def test_get_all_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_category_by_id():
    response = client.get("/categories/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_category():
    response = client.put("/categories/1", json={"name": "Updated Electronics"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Electronics"

def test_delete_category():
    response = client.delete("/categories/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Category deleted successfully"

# --------------------
# Item Tests
# --------------------

def test_create_item():
    # First recreate category
    client.post("/categories/", json={"name": "Gadgets"})

    item_data = {
        "name": "Smartphone",
        "description": "A phone with smart features",
        "price": 699.99,
        "is_offer": True,
        "rating": 4.5,
        "tags": "mobile,android",
        "stock_quantity": 10,
        "category_id": 2
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Smartphone"

def test_get_all_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_item_by_id():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_item():
    update_data = {
        "name": "Updated Smartphone",
        "description": "Updated description",
        "price": 749.99,
        "is_offer": False,
        "rating": 4.7,
        "tags": "updated,mobile",
        "stock_quantity": 15,
        "category_id": 2
    }
    response = client.put("/items/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Smartphone"

def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Item deleted successfully"
