from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operation on items.")

@blp.route("/item/<int:itemID>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, itemID:int) -> dict:
        item = ItemModel.query.get_or_404(itemID)
        return item
    
    @jwt_required()
    def delete(self, itemID:int) -> dict:
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401,
                  message="Admin privilege required.")
            
        item = ItemModel.query.get_or_404(itemID)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}
    
    # Update item
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, itemData:dict, itemID:int) -> dict:
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
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self) -> dict:
        return ItemModel.query.all()
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)    
    @blp.response(201, ItemSchema)
    def post(self, itemData:dict) -> dict:
        item = ItemModel(**itemData)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting items.")
        

        return item, 201