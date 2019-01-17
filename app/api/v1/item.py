# coding: utf-8
from flask_restful import Resource


class Item(Resource):
    def get(self):
        """获取所有条目"""
        pass

    def post(self):
        """创建一个条目"""
        pass


class ItemMember(Resource):
    def get(self, item_id):
        """获取一个条目的详情"""
        pass

    def put(self, item_id):
        """更新一个条目的信息"""
        pass

    def delete(self, item_id):
        """删除一个条目"""
        pass
