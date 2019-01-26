# coding: utf-8
from flask_restful import Resource, fields, marshal_with
from app.models import Item as ItemM, Category as CategoryM, Record as RecordM
from flask import abort, request
from app.utils import create_or_raise, get_or_raise,  MissingFormData, RedundantUpdate, TimeStamp, ReadableTime
from app.exts import db
from .record import query_filter


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
            'start': ReadableTime(attribute='start'),
            'start_stamp': TimeStamp(attribute='start'),
            'finish': ReadableTime(attribute='finish'),
            'finish_stamp': TimeStamp(attribute='finish'),
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
            'start': ReadableTime(attribute='start'),
            'start_stamp': TimeStamp(attribute='start'),
            'finish': ReadableTime(attribute='finish'),
            'finish_stamp': TimeStamp(attribute='finish'),
            'remark': fields.String
        }))
    }))
}

calculation_fields = {
    'status': fields.Integer,
    'message': fields.String,
    'data': fields.List(fields.Nested({
        'name': fields.String,
        'value': fields.Integer
    }))
}


class Item(Resource):
    """
    /item
    """
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
            item = create_or_raise(ItemM, name=name)
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
    """
    /item/<int:item_id>
    """
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
            category = get_or_raise(CategoryM, id=category_id)
            item = create_or_raise(ItemM, name=name)
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


class CalcOfItem(Resource):
    """
    /category/<int:category_id>/calculation
    """
    @marshal_with(calculation_fields)
    def get(self, category_id):
        """获取一个分类下的所有条目的记录的时间总和（秒）"""
        query = RecordM.query.join(RecordM.item).filter(ItemM.category_id == category_id)
        records = query_filter(query).all()
        if records and not records[-1].finish:
            records.pop()
        calc_dict = {}
        for x in records:
            if x.item.name in calc_dict.keys():
                calc_dict[x.item.name] += (x.finish.timestamp() - x.start.timestamp())
            else:
                calc_dict[x.item.name] = (x.finish.timestamp() - x.start.timestamp())
        calc_list = [x for x in calc_dict.items()]
        calc_list.sort(key=lambda x: x[1], reverse=True)
        res = [{'name': x[0], 'value':x[1]} for x in calc_list]
        return {
            'status': 200,
            'message': 'OK',
            'data': res
        }
