# coding: utf-8
from flask_restful import Resource


class Tag(Resource):
    def get(self):
        """获取所有标签"""
        pass

    def post(self):
        """创建一个标签"""
        pass


class TagMember(Resource):
    def get(self, tag_id):
        """获取一个标签的详情"""
        pass

    def put(self, tag_id):
        """更新一个标签的信息"""
        pass

    def delete(self, tag_id):
        """删除一个标签"""
        pass
