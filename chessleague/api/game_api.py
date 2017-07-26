from datetime import datetime

from flask import request

from chessleague.models import Game, db
from chessleague.decorators import etag, paginate, json
from chessleague.api import api, API_BASE_URL


@api.route(API_BASE_URL + '/games/', methods=['GET'])
@etag
@paginate()
def get_games():
    return Game.query


@api.route(API_BASE_URL + '/games/<int:id>', methods=['GET'])
@etag
@json
def get_game(id):
    return Game.query.get_or_404(id)


@api.route(API_BASE_URL + '/games/', methods=['POST'])
@json
def new_game():
    game = Game().from_json(request.json)
    db.session.add(game)
    db.session.commit()
    return {}, 201, {'Location': game.get_url()}


@api.route(API_BASE_URL + '/games/<int:id>', methods=['PUT'])
@json
def edit_game(id):
    game = Game.query.get_or_404(id)
    game.from_json(request.json)
    db.session.add(game)
    db.session.commit()
    return {}


@api.route(API_BASE_URL + '/games/<int:id>', methods=['DELETE'])
@json
def delete_game(id):
    game = Game.query.get_or_404(id)
    game.deleted = True
    db.session.commit()
    return {}, 204
