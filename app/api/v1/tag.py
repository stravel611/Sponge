# coding: utf-8
from flask_restful import Resource, fields, marshal_with
from app.models import Item as ItemM, Category as CategoryM, Tag as TagM, Record as RecordM
from flask import abort, request
from app.utils import get_or_create, get_or_raise,  MissingFormData, TimeStamp, ReadableTime
from app.exts import db


single_tag_fields = {
    'status': fields.Integer,
    'message': fields.String,
    'data': fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'recent_records': fields.List(fields.Nested({
            'id': fields.Integer,
            'start': ReadableTime(attribute='start'),
            'start_stamp': TimeStamp(attribute='start'),
            'finish': ReadableTime(attribute='finish'),
            'finish_stamp': TimeStamp(attribute='finish'),
            'remark': fields.String
        }))
    })
}

multi_tags_fields = {
    'status': fields.Integer,
    'message': fields.String,
    'data': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'recent_records': fields.List(fields.Nested({
            'id': fields.Integer,
            'start': ReadableTime(attribute='start'),
            'start_stamp': TimeStamp(attribute='start'),
            'finish': ReadableTime(attribute='finish'),
            'finish_stamp': TimeStamp(attribute='finish'),
            'remark': fields.String
        }))
    }))
}


class Tag(Resource):
    """
    /tag
    """
    @marshal_with(multi_tags_fields)
    def get(self):
        """获取所有标签"""
        tags = TagM.query.all()
        return {
            'status': 200,
            'message': 'OK',
            'data': tags
        }


class TagMember(Resource):
    """
    /tag/<int:tag_id>
    """
    @marshal_with(single_tag_fields)
    def get(self, tag_id):
        """获取一个标签的详情"""
        tag = TagM.query.get(tag_id)
        if tag:
            return {
                'status': 200,
                'message': 'OK',
                'data': tag
            }
        else:
            abort(404)


class TagOfCategory(Resource):
    """
    /category/<int:category_id>/tag
    """
    @marshal_with(multi_tags_fields)
    def get(self, category_id):
        """获取一个分类下的所有标签"""
        tags = TagM.query.join(TagM.records).join(RecordM.item)\
            .filter(CategoryM.id == category_id).all()
        return {
            'status': 200,
            'message': 'OK',
            'data': tags
        }


class TagOfItem(Resource):
    """
    /item/<int:item_id>/tag
    """
    @marshal_with(multi_tags_fields)
    def get(self, item_id):
        """获取一个条目下的所有标签"""
        tags = TagM.query.join(TagM.records).filter(ItemM.id == item_id)
        return {
            'status': 200,
            'message': 'OK',
            'data': tags
        }


class TagOfRecord(Resource):
    """
    /record/<int:record_id>/tag
    """
    @marshal_with(single_tag_fields)
    def post(self, record_id):
        """在一条记录下创建一个标签"""
        name = request.form.get('name', '')
        if name:
            record = get_or_raise(RecordM, id=record_id)
            tag = get_or_create(TagM, name=name)
            tag.records.append(record)
            db.session.add(tag)
            db.session.commit()
            return {
               'status': 201,
               'message': 'Created',
               'data': tag
            }, 201
        else:
            raise MissingFormData()

    def delete(self, record_id):
        """在一条记录下删除一个标签"""
        tag_id = request.args.get('id', type=int)
        if tag_id:
            record = get_or_raise(RecordM, id=record_id)
            tag = get_or_raise(TagM, id=tag_id)
            record.tags.remove(tag)
            db.session.add(record)
            db.session.commit()
            return {
                'status': 200,
                'message': 'OK',
                'data': None
            }
        else:
            raise MissingFormData()
