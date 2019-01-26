# coding: utf-8
from faker import Faker
from app.models import Category, Item, Record, Tag
from app.exts import db
import random
from sqlalchemy.exc import IntegrityError


fake = Faker('zh_CN')


def fake_categories(count=5):
    while True:
        try:
            for _ in range(count):
                category = Category(name=fake.word())
                db.session.add(category)
            db.session.commit()
            break
        except IntegrityError:
            db.session.rollback()
            continue


def fake_items(count=20):
    categories = Category.query.all()
    while True:
        try:
            for _ in range(count):
                item = Item(name=fake.word())
                item.category = random.choice(categories)
                db.session.add(item)
            db.session.commit()
            break
        except IntegrityError:
            db.session.rollback()
            continue


def fake_records(count=50):
    items = Item.query.all()
    times = [fake.date_time_this_year() for _ in range(count * 2)]
    times.sort(reverse=True)
    while True:
        try:
            for _ in range(count):
                record = Record(
                    start=times.pop(),
                    finish=times.pop(),
                    remark=fake.sentence()
                )
                record.item = random.choice(items)
                db.session.add(record)
            db.session.commit()
            break
        except IntegrityError:
            db.session.rollback()
            continue


def fake_tags(count=10):
    records = Record.query.all()
    while True:
        try:
            for _ in range(count):
                tag = Tag(name=fake.word())
                tag.records = random.sample(records, k=random.randint(0, len(records)))
                db.session.add(tag)
            db.session.commit()
            break
        except IntegrityError:
            db.session.rollback()
            continue
