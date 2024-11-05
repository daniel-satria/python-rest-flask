from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operation on items.")

@blp.route("/item/<string:itemID>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, itemID):
        item = ItemModel.query.get_or_404(itemID)
        return item
            
    def delete(self, itemID):
        item = ItemModel.query.get_or_404(itemID)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}
    
    # Update item
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, itemData, itemID):
        item = ItemModel.query.get(itemID)
        if item:
            item.price = itemData["price"]
            item.name = itemData["name"]
        else:
            item = ItemModel(id=itemID, **itemData)

        db.session.add(item)
        db.session.commit()
        
        return item
    
@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @blp.arguments(ItemSchema)    
    @blp.response(201, ItemSchema)
    def post(self, itemData):
        item = ItemModel(**itemData)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting items.")
        
        
        return item, 201