from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemsSchema

blp = Blueprint("Tags", "tags", description="Operation on tags")

@blp.route("/store/<int:store_id>/tag")
class TagsInstore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id:str) -> dict:
        store = StoreModel.query.get_or_404(store_id)
        
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data:dict, store_id:int) -> dict:
        if TagModel.query.filter(TagModel.store_id == store_id,
                                 TagModel.name == tag_data["name"]).first():
            abort(400,
                  message="A tag with that name already exists in the store.")
        
        tag = TagModel(**tag_data, store_id=store_id)
        
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,
                  message=str(e)
            )
            
        return tag
    
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id:int, tag_id:int) -> dict:
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        item.tags.append(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,
                  message="An error occured while inserting the tag."
            )
            
        return tag
    
    @blp.response(200, TagAndItemsSchema)
    def delete(self, item_id:int, tag_id:int) -> dict:
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        item.tags.remove(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,
                  message="An error occurred when deleting tags."
            )
            
        return {"message": "Item removed from tag", "item": item, "tag":tag}
    
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id:int) -> dict:
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."}
    )
    @blp.alt_response(
        404,
        description="Tag not found."
    )
    @blp.alt_response(
        400,
        description="Returned if tag is assigned to one or more items. In this case, the tag is not deleted."
    )
    def delete(self, tag_id:str) -> dict:
        tag = TagModel.query.get_or_404(tag_id)
        
        if not tag.items:
            db.session.add(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again."
        )