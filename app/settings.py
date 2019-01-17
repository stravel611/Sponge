# coding: utf-8
import os


root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if os.name == 'nt':
    sqlite3 = 'sqlite:///'
else:
    sqlite3 = 'sqlite:////'


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = sqlite3 + os.path.join(root_path, 'data.db')
