# coding: utf-8
from flask import Flask
from app.settings import Config
from app.exts import db
from app.bp_api import api
import click
from app.models import Category, Item, Record, Tag, record_tag


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


app.register_blueprint(api)
@app.cli.command()
def init_db():
    click.echo('正在初始化数据库...')
    db.drop_all()
    db.create_all()
    click.echo('数据库初始化完毕！')


if __name__ == '__main__':
    app.run(port=5000)
