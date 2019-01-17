# coding: utf-8
from flask import Blueprint
from flask_restful import Api, Resource


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)


class Test(Resource):
    def get(self):
        return {'status': 'OK'}


api.add_resource(Test, '/test')
