from flask import Flask, request
from db import stores, items
from flask_smorest import abort
import uuid

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = ({**item_data, "id": item_id})
    return item, 201


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")
def get_item_(item_id: str):
    try:
        return items[item_id], 201
    except KeyError:
        abort(404, message="item not found")

@app.get("/store/<string:store_id>")
def get_store_info(store_id: str):
    try:
        return stores[store_id], 201
    except KeyError:
        abort(404, message="Store not found")
