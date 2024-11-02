import sys
import os
from fastapi.testclient import TestClient
from main import app
from models.models import Sheep
from models.db import db  # Assuming `db` is the instance of `FakeDB`

# Add the project root (sheep directory) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

def test_read_sheep():
    response = client.get("/sheep/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

def test_add_sheep():
    new_sheep = {
        "id": 10,
        "name": "Babydoll",
        "breed": "Gotland",
        "sex": "ewe"
    }
    response = client.post("/sheep/", json=new_sheep)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data == new_sheep

    retrieve_response = client.get(f"/sheep/{new_sheep['id']}")
    assert retrieve_response.status_code == 200
    assert retrieve_response.json() == new_sheep

def test_read_all_sheep():
    response = client.get("/sheep/")
    assert response.status_code == 200

    all_sheep = response.json()
    assert isinstance(all_sheep, list)
    assert len(all_sheep) == len(db.data)

def test_delete_sheep():
    response = client.delete("/sheep/1")
    assert response.status_code == 204

    get_response = client.get("/sheep/1")
    assert get_response.status_code == 404

def test_update_sheep():
    update_sheep = {
        "id": 2,
        "name": "Sugar",
        "breed": "Polypay",
        "sex": "ram"
    }
    response = client.put("/sheep/2", json=update_sheep)
    assert response.status_code == 200
    assert response.json() == update_sheep

    get_response = client.get("/sheep/2")
    assert get_response.status_code == 200
    assert get_response.json() == update_sheep
