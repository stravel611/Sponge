# coding: utf-8
from app.exts import db
from werkzeug.exceptions import BadRequest, Conflict, NotFound


def create_or_raise(model, key, value):
    item = model.query.filter(getattr(model, key) == value).first()
    if not item:
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


class MissingFormData(BadRequest):
    """表单参数缺失"""


class AlreadyExisted(Conflict):
    """新建项目，而项目已经存在"""


class RedundantUpdate(Conflict):
    """请求更新内容与原内容相同"""
