# coding: utf-8
from app.exts import db
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from flask_restful.fields import Raw


def create_or_raise(model, key, value):
    item = model.query.filter(getattr(model, key) == value).first()
    if item is None:
        item = model()
        setattr(item, key, value)
        db.session.add(item)
        db.session.commit()
        return item
    else:
        raise AlreadyExisted()


def check_or_raise(model, key, value):
    item = model.query.filter(getattr(model, key) == value).first()
    if item:
        return item
    else:
        raise NotFound()


def get_or_create(model, key, value):
    item = model.query.filter(getattr(model, key) == value).first()
    if item is None:
        item = model()
        setattr(item, key, value)
        db.session.add(item)
        db.session.commit()
    return item


class MissingFormData(BadRequest):
    """表单参数缺失"""


class AlreadyExisted(Conflict):
    """新建项目，而项目已经存在"""


class RedundantUpdate(Conflict):
    """请求更新内容与原内容相同"""


class ParseToTimeStamp(Raw):
    def format(self, value):
        return value.timestamp() * 1000


class ReadableTime(Raw):
    def format(self, value):
        hour = value.hour if value.hour >=10 else '0'+str(value.hour)
        minute = value.minute if value.minute >= 10 else '0'+str(value.minute)
        second = value.second if value.second >= 10 else '0'+str(value.second)
        return f'{value.month}月{value.day}日 {hour}:{minute}:{second}'
