from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep

app = FastAPI()

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    sheep = db.get_sheep(id)
    if sheep is None:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return sheep




@app.post("/sheep/", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    if sheep.id in db.data:  # Check if the sheep ID already exists
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sheep with this id already exists")
    db.data[sheep.id] = sheep
    return sheep

@app.delete("/sheep/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sheep(id: int):
    sheep = db.get_sheep(id)
    if sheep is None:
        raise HTTPException(status_code=404, detail="Sheep not found")
    del db.data[id]
    return

@app.put("/sheep/{id}", response_model= Sheep)
def update_sheep(id:int, sheep: Sheep):
    existing_sheep = db.get_sheep(id)
    if existing_sheep is None:
        raise HTTPException(status_code=404, detail="Sheep not found")
    db.data[id] = sheep
    return sheep

@app.get("/sheep/{id}", response_model=list[Sheep])
def read_all_sheep():
    return list(db.data.values())
