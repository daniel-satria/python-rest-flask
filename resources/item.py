import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import ItemSchema, ItemUpdateSchema
from db import items, stores

blp = Blueprint("Items", __name__, description="Operation on items.")

@blp.route("/item/<string:itemID>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
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
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, itemData, itemID):
        try:
            item = items[itemID]

            # https://blog.teclado.com/python-dictionary-merge-update-operators/
            item |= itemData

            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)    
    @blp.response(201, ItemSchema)
    def post(self, itemData):
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