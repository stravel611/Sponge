# coding: utf-8
from flask import Flask
from app.settings import Config
from app.exts import db


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


if __name__ == '__main__':
    app.run(port=5000)
