# coding: utf-8
from app.exts import db


record_tag = db.Table(
    'record_tag',
    db.Column('record_id', db.Integer, db.ForeignKey('record.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    items = db.relationship('Item', back_populates='category')


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = db.relationship('Category', back_populates='items')
    records = db.relationship('Record', back_populates='item')

    @property
    def recent_records(self):
        return list(reversed(self.records[-5:]))


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    finish = db.Column(db.DateTime)
    remark = db.Column(db.String(120))

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    item = db.relationship('Item', back_populates='records')
    tags = db.relationship('Tag', secondary=record_tag, back_populates='records')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    records = db.relationship('Record', secondary=record_tag, back_populates='tags')
