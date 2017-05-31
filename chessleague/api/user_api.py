from flask import request

from chessleague import app
from chessleague.models import db, User

from chessleague.api import api
from chessleague.decorators import etag, paginate, json

@api.route('/users/', methods=['GET'])
@etag
@paginate()
def get_users():
    return User.query

@api.route('/users/<int:id>', methods=['GET'])
@etag
@json
def get_user(id):
    return User.query.get_or_404(id)

@api.route('/users/<int:id>/team/', methods=['GET'])
@etag
@paginate()
def get_user_team(id):
    user = User.query.get_or_404(id)
    return user.team

@api.route('/users/', methods=['POST'])
@json
def new_user():
    user = User().from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return {}, 201, {'Location': user.get_url()}

@api.route('/users/<int:id>', methods=['PUT'])
@json
def edit_user(id):
    user = User.query.get_or_404(id)
    user.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return {}

@api.route('/users/<int:id>', methods=['DELETE'])
@json
def delete_user(id):
    user = User.query.get_or_404(id)
    user.active = False
    db.session.commit()
    return {}
