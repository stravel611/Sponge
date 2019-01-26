# coding: utf-8
from app.exts import db
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from flask_restful.fields import Raw


#-------------------------数据库模型工具-------------------------
def create_or_raise(model, **kwargs):
    """尝试在一个模型下创建一条记录，如果已存在则抛出异常"""
    item = model.query
    for k, v in kwargs.items():
        item = item.filter(getattr(model,k) == v)
    if item.first() is None:
        item = model()
        for k, v in kwargs.items():
            setattr(item, k, v)
        db.session.add(item)
        db.session.commit()
        return item
    else:
        raise AlreadyExisted()


def get_or_raise(model, **kwargs):
    """尝试在一个模型下查找一条记录，如果不存在则抛出异常"""
    item = model.query
    for k, v in kwargs.items():
        item = item.filter(getattr(model, k) == v)
    item = item.first()
    if item:
        return item
    else:
        raise NotFound()


def get_or_create(model, **kwargs):
    """尝试在一个模型下查找一条记录，如果不存在则创建记录"""
    item = model.query
    for k, v in kwargs.items():
        item = item.filter(getattr(model, k) == v)
    item = item.first()
    if item is None:
        item = model()
        for k, v in kwargs.items():
            setattr(item, k, v)
        db.session.add(item)
        db.session.commit()
    return item


#-------------------------异常-------------------------
class MissingFormData(BadRequest):
    """表单参数缺失"""


class AlreadyExisted(Conflict):
    """新建项目，而项目已经存在"""


class RedundantUpdate(Conflict):
    """请求更新内容与原内容相同"""


#-------------------------API 响应格式化工具-------------------------
class TimeStamp(Raw):
    def format(self, value):
        return value.timestamp() * 1000


class ReadableTime(Raw):
    """将 datetime 转化为如 '3月16日 08:46:02' 的格式"""
    def format(self, value):
        hour = value.hour if value.hour >=10 else '0'+str(value.hour)
        minute = value.minute if value.minute >= 10 else '0'+str(value.minute)
        second = value.second if value.second >= 10 else '0'+str(value.second)
        return f'{value.month}月{value.day}日 {hour}:{minute}:{second}'
