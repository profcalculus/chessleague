from flask import request

from chessleague.models import User, db
from chessleague.errors import ValidationError
from . import api, auth, API_BASE_URL

from chessleague.decorators import etag, paginate, json

@api.route(API_BASE_URL + '/users/', methods=['GET'])
@etag
@paginate()
def get_users():
    return User.query


@api.route(API_BASE_URL + '/users/<int:id>', methods=['GET'])
@etag
@json
def get_user(id):
    return User.query.get_or_404(id)


@api.route(API_BASE_URL + '/users/<int:id>/team/', methods=['GET'])
@etag
@paginate()
def get_user_team(id):
    user = User.query.get_or_404(id)
    return user.team


@api.route(API_BASE_URL + '/users/', methods=['POST'])
@json
@auth.login_required
def new_user():
    user = User().from_json(request.json)
    if user.user_name is None or user.password_hash is None:
        raise ValidationError('user_name and password are required.')
    db.session.add(user)
    db.session.commit()
    return {}, 201, {'Location': user.get_url()}


@api.route(API_BASE_URL + '/users/<int:id>', methods=['PUT'])
@json
# @auth.login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    user.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return {}


@api.route(API_BASE_URL + '/users/<int:id>', methods=['DELETE'])
@json
@auth.login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    user.deleted = True
    db.session.commit()
    return {}, 204
