# coding: utf-8
from flask import Blueprint
from flask_restful import Api
from .category import Category, CategoryMember, CalcOfCategory
from .item import Item, ItemMember, ItemOfCategory, CalcOfItem
from .record import Record, RecordMember, RecordOfCategory, RecordOfItem
from .tag import Tag, TagMember, TagOfCategory, TagOfItem, TagOfRecord


errors = {
    'BadRequest': {
        'status': 400,
        'message': '请求错误。'
    },
    'MissingFormData': {
        'status': 400,
        'message': '表单数据缺失，请检查表单数据是否完整，类型是否正确。'
    },
    'NotFound': {
        'status': 404,
        'message': '没有找到请求的资源。'
    },
    'AlreadyExisted': {
        'status': 409,
        'message': '资源已存在，无需创建；或者检查请求参数是否有误。'
    },
    'RedundantUpdate': {
        'status': 409,
        'message': '请求更新的内容与原内容相同，无需更新；或者检查更新内容是否有误。'
    }
}


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


api = Api(api_bp, errors=errors)
api.add_resource(Category, '/category')
api.add_resource(CategoryMember, '/category/<int:category_id>')
api.add_resource(CalcOfCategory, '/category/calculation')
api.add_resource(CalcOfItem, '/category/<int:category_id>/calculation')
api.add_resource(Item, '/item')
api.add_resource(ItemMember, '/item/<int:item_id>')
api.add_resource(ItemOfCategory, '/category/<int:category_id>/item')
api.add_resource(Record, '/record')
api.add_resource(RecordMember, '/record/<int:record_id>')
api.add_resource(RecordOfCategory, '/category/<int:category_id>/record')
api.add_resource(RecordOfItem, '/item/<int:item_id>/record')
api.add_resource(Tag, '/tag')
api.add_resource(TagMember, '/tag/<int:tag_id>')
api.add_resource(TagOfCategory, '/category/<int:category_id>/tag')
api.add_resource(TagOfItem, '/item/<int:item_id>/tag')
api.add_resource(TagOfRecord, '/record/<int:record_id>/tag')
