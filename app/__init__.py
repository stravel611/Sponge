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


@app.after_request
def add_header(res):
    res.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    return res


@app.errorhandler(404)
def handle_404(err):
    return jsonify({'status': 404, 'message': 'Not Found.'}), 404


@app.cli.command()
def init_db():
    click.echo('正在初始化数据库...')
    db.drop_all()
    db.create_all()
    click.echo('数据库初始化完毕！')


@app.cli.command()
@click.option('--drop', is_flag=True, help='删除已存在的表')
def forge(drop):
    if drop:
        click.echo('正在初始化数据库...')
        db.drop_all()
        db.create_all()
        click.echo('数据库初始化完毕！')
    click.echo('正在生成分类...')
    fake.fake_categories()
    click.echo('正在生成条目...')
    fake.fake_items()
    click.echo('正在生成记录...')
    fake.fake_records()
    click.echo('正在生成标签...')
    fake.fake_tags()
    click.echo('数据生成完毕！')


if __name__ == '__main__':
    app.run(port=5000)
