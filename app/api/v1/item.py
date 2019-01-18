# coding: utf-8
from flask_restful import Resource, fields, marshal_with
from app.models import Item as ItemM, Category as CategoryM
from flask import abort, request
from app.utils import create_or_raise, check_or_raise,  MissingFormData, RedundantUpdate
from app.exts import db


single_item_fields = {
    'status': fields.Integer,
    'message': fields.String,
    'data': fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'category': fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        }),
        'recent_records': fields.List(fields.Nested({
            'id': fields.Integer,
            'start': fields.DateTime(dt_format='iso8601'),
            'finish': fields.DateTime(dt_format='iso8601'),
            'remark': fields.String
        }))
    })
}

multi_items_fields = {
    'status': fields.Integer,
    'message': fields.String,
    'data': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'category': fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        }),
        'recent_records': fields.List(fields.Nested({
            'id': fields.Integer,
            'start': fields.DateTime(dt_format='iso8601'),
            'finish': fields.DateTime(dt_format='iso8601'),
            'remark': fields.String
        }))
    }))
}


class Item(Resource):
    @marshal_with(multi_items_fields)
    def get(self):
        """获取所有条目"""
        items = ItemM.query.all()
        return {
            'status': 200,
            'message': 'OK',
            'data': items
        }

    @marshal_with(single_item_fields)
    def post(self):
        """创建一个条目"""
        name = request.form.get('name', '')
        if name:
            item = create_or_raise(ItemM, 'name', name)
            db.session.add(item)
            db.session.commit()
            return {
               'status': 201,
               'message': 'Created',
               'data': item
            }, 201
        else:
            raise MissingFormData()


class ItemMember(Resource):
    @marshal_with(single_item_fields)
    def get(self, item_id):
        """获取一个条目的详情"""
        item = ItemM.query.get(item_id)
        if item:
            return {
                'status': 200,
                'message': 'OK',
                'data': item
            }
        else:
            abort(404)

    @marshal_with(single_item_fields)
    def put(self, item_id):
        """更新一个条目的信息"""
        item = ItemM.query.get(item_id)
        if item is None:
            abort(404)
        name = request.form.get('name', '')
        if name:
            if item.name == name:
                raise RedundantUpdate()
            else:
                item.name = name
                db.session.add(item)
                db.session.commit()
                return {
                    'status': 200,
                    'message': 'OK',
                    'data': item
                }
        else:
            raise MissingFormData()

    def delete(self, item_id):
        """删除一个条目"""
        item = ItemM.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return {
                'status': 200,
                'message': 'OK',
                'data': None
            }
        else:
            abort(404)


class ItemOfCategory(Resource):
    @marshal_with(multi_items_fields)
    def get(self, category_id):
        """获取一个分类下的所有条目"""
        items = ItemM.query.filter_by(category_id=category_id).all()
        return {
            'status': 200,
            'message': 'OK',
            'data': items
        }

    @marshal_with(single_item_fields)
    def post(self, category_id):
        """在一个分类下创建一个条目"""
        name = request.form.get('name', '')
        if name:
            category = check_or_raise(CategoryM, 'id', category_id)
            item = create_or_raise(ItemM, 'name', name)
            item.category = category
            db.session.add(item)
            db.session.commit()
            return {
               'status': 201,
               'message': 'Created',
               'data': item
            }, 201
        else:
            raise MissingFormData()
