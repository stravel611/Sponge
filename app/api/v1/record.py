# coding: utf-8
from flask_restful import Resource, fields, marshal_with
from app.models import Record as RecordM, Item as ItemM, Category as CategoryM
from flask import abort, request
from app.utils import MissingFormData, RedundantUpdate
from app.exts import db
from datetime import datetime


single_record_fields = {
    'status': fields.Integer,
    'message': fields.String,
    'data': fields.Nested({
        'id': fields.Integer,
        'start': fields.DateTime(dt_format='iso8601'),
        'finish': fields.DateTime(dt_format='iso8601'),
        'item': fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        }),
        'tags': fields.List(fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        }))
    })
}

multi_records_fields = {
    'status': fields.Integer,
    'message': fields.String,
    'data': fields.List(fields.Nested({
        'id': fields.Integer,
        'start': fields.DateTime(dt_format='iso8601'),
        'finish': fields.DateTime(dt_format='iso8601'),
        'item': fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        }),
        'tags': fields.List(fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        }))
    }))
}


class Record(Resource):
    @marshal_with(multi_records_fields)
    def get(self):
        """获取所有记录"""
        records = RecordM.query.all()
        return {
            'status': 200,
            'message': 'OK',
            'data': records
        }


class RecordMember(Resource):
    @marshal_with(single_record_fields)
    def get(self, record_id):
        """获取一条记录的详情"""
        record = RecordM.query.get(record_id)
        if record:
            return {
                'status': 200,
                'message': 'OK',
                'data': record
            }
        else:
            abort(404)

    @marshal_with(single_record_fields)
    def put(self, record_id):
        """更新一条记录的信息"""
        record = RecordM.query.get(record_id)
        if record is None:
            abort(404)
        finish_stamp = request.form.get('finish', type=int)
        remark = request.form.get('remark')
        if finish_stamp:
            finish = datetime.fromtimestamp(finish_stamp / 1000)
            record.finish = finish
            db.session.add(record)
            db.session.commit()
            return {
                'status': 200,
                'message': 'OK',
                'data': record
            }
        elif remark:
            if record.remark == remark:
                raise RedundantUpdate()
            else:
                record.remark = remark
                db.session.add(record)
                db.session.commit()
                return {
                    'status': 200,
                    'message': 'OK',
                    'data': record
                }
        else:
            raise MissingFormData()

    def delete(self, record_id):
        """删除一条记录"""
        record = ItemM.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return {
                'status': 200,
                'message': 'OK',
                'data': None
            }
        else:
            abort(404)


class RecordOfCategory(Resource):
    @marshal_with(multi_records_fields)
    def get(self, category_id):
        """获取一个分类下的所有记录"""
        records = RecordM.query.join(RecordM.item)\
            .filter(CategoryM.id==category_id).all()
        return {
            'status': 200,
            'message': 'OK',
            'data': records
        }


class RecordOfItem(Resource):
    @marshal_with(multi_records_fields)
    def get(self, item_id):
        """获取一个条目选的所有记录"""
        records = RecordM.query.filter_by(item_id=item_id).all()
        return {
            'status': 200,
            'message': 'OK',
            'data': records
        }

    @marshal_with(single_record_fields)
    def post(self, item_id):
        """在一个条目下创建一条记录"""
        start_stamp = request.form.get('start', type=int)
        remark = request.form.get('remark', '')
        if start_stamp:
            start = datetime.fromtimestamp(start_stamp / 1000)
            record = RecordM(start=start, remark=remark)
            db.session.add(record)
            db.session.commit()
            return {
               'status': 201,
               'message': 'Created',
               'data': record
            }, 201
        else:
            raise MissingFormData()