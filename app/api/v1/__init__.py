# coding: utf-8
from flask import Blueprint
from flask_restful import Api
from .category import Category, CategoryMember
from .item import Item, ItemMember
from .record import Record, RecordMember
from .tag import Tag, TagMember

errors = {
    'NotFound': {
        'status': 404,
        'message': 'Not Found.',
        'data': None
    }
}


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp, errors=errors)


api.add_resource(Category, '/category')
api.add_resource(CategoryMember, '/category/<int:category_id>')
api.add_resource(Item, '/item')
api.add_resource(ItemMember, '/item/<int:item_id>')
api.add_resource(Record, '/record')
api.add_resource(RecordMember, '/record/<int:record_id>')
api.add_resource(Tag, '/tag')
api.add_resource(TagMember, '/tag/<int:tag_id>')
