# coding: utf-8
from flask_restful import Resource, fields, marshal_with
from app.models import Category as CategoryM
from flask import abort, request
from app.utils import create_or_raise, MissingFormData, RedundantUpdate
from app.exts import db


single_category_fields = {
    'status': fields.Integer,
    'message': fields.String,
    'data': fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'items': fields.List(fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        }))
    })
}

multi_categories_fields = {
    'status': fields.Integer,
    'message': fields.String,
    'data': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'items': fields.List(fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        }))
    }))
}


class Category(Resource):
    @marshal_with(multi_categories_fields)
    def get(self):
        """获取所有分类"""
        categories = CategoryM.query.all()
        return {
            'status': 200,
            'message': 'OK',
            'data': categories
        }

    @marshal_with(single_category_fields)
    def post(self):
        """创建一个分类"""
        name = request.form.get('name', '')
        if name:
            category = create_or_raise(CategoryM, 'name', name)
            return {
                'status': 201,
                'message': 'Created',
                'data': category
            }, 201
        else:
            raise MissingFormData()


class CategoryMember(Resource):
    @marshal_with(single_category_fields)
    def get(self, category_id):
        """获取一个分类的详情"""
        category = CategoryM.query.get(category_id)
        if category:
            return {
                'status': 200,
                'message': 'OK',
                'data': category
            }
        else:
            abort(404)

    @marshal_with(single_category_fields)
    def put(self, category_id):
        """更新一个分类的信息"""
        category = CategoryM.query.get(category_id)
        if category is None:
            abort(404)
        name = request.form.get('name', '')
        if name:
            if category.name == name:
                raise RedundantUpdate()
            else:
                category.name = name
                db.session.add(category)
                db.session.commit()
                return {
                    'status': 200,
                    'message': 'OK',
                    'data': category
                }
        else:
            raise MissingFormData()

    def delete(self, category_id):
        """删除一个分类"""
        category = CategoryM.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return {
                'status': 200,
                'message': 'OK',
                'data': None
            }
        else:
            abort(404)
