# coding: utf-8
from flask_restful import Resource, fields, marshal_with
from app.models import Category as CategoryM
from flask import abort


class Category(Resource):
    def get(self):
        """获取所有分类"""
        pass

    def post(self):
        """创建一个分类"""
        pass


class CategoryMember(Resource):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'items': fields.List(fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        }))
    }

    @marshal_with(resource_fields)
    def get(self, category_id):
        """获取一个分类的详情"""
        category = CategoryM.query.get(category_id)
        if category:
            return category
        else:
            abort(404)

    def put(self, category_id):
        """更新一个分类的信息"""
        pass

    def delete(self, category_id):
        """删除一个分类"""
