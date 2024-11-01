import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores

blp = Blueprint("Items", __name__, description="Operation on items.")

@blp.route("/item/<string:itemID>")
class Item(MethodView):
    def get(self, itemID):
        try:
            return items[itemID]
        except KeyError:
            abort(404, message="Item not found.")
            
    def delete(self, itemID):
        try:
            del items[itemID]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    # Update item
    def put(self, itemID):
        item_data = request.get_json()
        # There's  more validation to do here!
        # Like making sure price is a number, and also both items are optional
        # Difficult to do with an if statement...
        if ("price" not in item_data) or ("name" not in item_data):
            abort(
                400,
                message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
            )
        try:
            item = items[itemID]

            # https://blog.teclado.com/python-dictionary-merge-update-operators/
            item |= item_data

            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}
    
    def post(self):
        itemData = request.get_json()
        
        if ("price" not in itemData or
            "store_id" not in itemData or
            "name" not in itemData
        ):
            abort(400, message="Bad request. Ensure price, store_id, and name included in JSON payload.")
            
        for item in items.values():
            if (
            itemData["name"] == item["name"] and
            itemData["store_id"] == item["store_id"]  
            ):
                abort(400, message=f"Item already exist.")
        
        if itemData["store_id"] not in stores:
            abort(404, message="Store not found!")
            
        itemID = uuid.uuid4().hex
        item = {**itemData, "id":itemID}
        items[itemID] = item
        
        return item, 201