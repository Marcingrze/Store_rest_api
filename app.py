from flask import Flask, request
from db import stores, items
import uuid

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201

@app.post("/store/<string:name>/item")
def add_item(name: str):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "store not found"}, 404

@app.get("/store/<string:name>/item")
def get_item_in_store(name: str):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}, 201
    return {"message": "store not found"}, 404

@app.get("/store/<string:store_id>")
def get_store_info(store_id : str):
    try:
        return stores[store_id], 201
    except KeyError:
        return {"message": "store not found"}, 404
