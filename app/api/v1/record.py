# coding: utf-8
from flask_restful import Resource


class Record(Resource):
    def get(self):
        """获取所有记录"""
        pass

    def post(self):
        """创建一条记录"""
        pass


class RecordMember(Resource):
    def get(self, record_id):
        """获取一条记录的详情"""
        pass

    def put(self, record_id):
        """更新一条记录的信息"""
        pass

    def delete(self, record_id):
        """删除一条记录"""
        pass
