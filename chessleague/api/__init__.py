from flask import jsonify
from flask_restful import Api
from chessleague import app

from base_request_parser import BaseRequestParser

from ipdb import set_trace as DBG

BASE_URL = app.config['BASE_URL']
api = Api(app)


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response
