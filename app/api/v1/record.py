# coding: utf-8
from flask_restful import Resource, fields, marshal_with
from app.models import Record as RecordM, Item as ItemM
from flask import abort, request
from app.utils import get_or_raise, MissingFormData, RedundantUpdate, TimeStamp, ReadableTime
from app.exts import db
from datetime import datetime


def query_filter(query):
    from_time = request.args.get('from', type=int)
    to_time = request.args.get('to', type=int)
    limit = request.args.get('limit', type=int)
    if from_time:
        query = query.filter(
            RecordM.start > datetime.fromtimestamp(from_time / 1000)
        )
    if to_time:
        query = query.filter(
            RecordM.start < datetime.fromtimestamp(to_time / 1000)
        )
    if limit:
        query = query.limit(limit)
    return query


single_record_fields = {
    'status': fields.Integer,
    'message': fields.String,
    'data': fields.Nested({
        'id': fields.Integer,
        'start': ReadableTime(attribute='start'),
        'start_stamp': TimeStamp(attribute='start'),
        'finish': ReadableTime(attribute='finish'),
        'finish_stamp': TimeStamp(attribute='finish'),
        'remark': fields.String,
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
        'start': ReadableTime(attribute='start'),
        'start_stamp': TimeStamp(attribute='start'),
        'finish': ReadableTime(attribute='finish'),
        'finish_stamp': TimeStamp(attribute='finish'),
        'remark': fields.String,
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
    """
    /record
    """
    @marshal_with(multi_records_fields)
    def get(self):
        """获取所有记录，按开始时间降序排序"""
        query = RecordM.query.order_by(RecordM.id.desc())
        records = query_filter(query).all()
        if records and not records[0].finish:
            records.pop(0)
        return {
            'status': 200,
            'message': 'OK',
            'data': records
        }


class RecordMember(Resource):
    """
    /record/<int:record_id>
    """
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
        record = RecordM.query.get(record_id)
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
    """
    /category/<int:category_id>/record
    """
    @marshal_with(multi_records_fields)
    def get(self, category_id):
        """获取一个分类下的所有记录，按开始时间降序排序"""
        query = RecordM.query.join(RecordM.item)\
            .filter(ItemM.category_id == category_id)\
            .order_by(RecordM.id.desc())
        records = query_filter(query).all()
        if records and not records[0].finish:
            records.pop(0)
        return {
            'status': 200,
            'message': 'OK',
            'data': records
        }


class RecordOfItem(Resource):
    """
    /item/<int:item_id>/record
    """
    @marshal_with(multi_records_fields)
    def get(self, item_id):
        """获取一个条目下的所有记录，按开始时间降序排序"""
        query = RecordM.query.filter_by(item_id=item_id).order_by(RecordM.id.desc())
        records = query_filter(query).all()
        return {
            'status': 200,
            'message': 'OK',
            'data': records
        }

    @marshal_with(single_record_fields)
    def post(self, item_id):
        """在一个条目下创建一条记录"""
        remark = request.form.get('remark', '')
        item = get_or_raise(ItemM, id=item_id)
        start = datetime.now()
        record = RecordM(start=start, remark=remark)
        record.item = item
        db.session.add(record)
        db.session.commit()
        return {
           'status': 201,
           'message': 'Created',
           'data': record
        }, 201


class RecordProceeding(Resource):
    """
    /record/proceeding
    """
    @marshal_with(single_record_fields)
    def get(self):
        """获取正在进行的记录"""
        record = RecordM.query.order_by(RecordM.id.desc()).first()
        if record and record.finish:
            record = None
        return {
            'status': 200,
            'message': 'OK',
            'data': record
        }
