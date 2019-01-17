# coding: utf-8
from flask import Flask, jsonify
from app.settings import Config
from app.exts import db
from app.api import api_bp_v1
import click
from app.models import Category, Item, Record, Tag, record_tag
import app.fakes as fake


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


app.register_blueprint(api_bp_v1)


@app.errorhandler(404)
def handle_404(err):
    return jsonify({'status': 404, 'message': 'Not Found.', 'data': None}), 404


@app.cli.command()
def init_db():
    click.echo('正在初始化数据库...')
    db.drop_all()
    db.create_all()
    click.echo('数据库初始化完毕！')


@app.cli.command()
def forge():
    db.drop_all()
    db.create_all()
    fake.fake_categories()
    fake.fake_items()
    fake.fake_records()
    fake.fake_tags()


if __name__ == '__main__':
    app.run(port=5000)
