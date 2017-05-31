from datetime import datetime

from flask import request

from chessleague import app
from chessleague.models import db, Game
from chessleague.decorators import etag, paginate, json
from chessleague.api import api

@api.route('/games/', methods=['GET'])
@etag
@paginate()
def get_games():
    return Game.query

@api.route('/games/<int:id>', methods=['GET'])
@etag
@json
def get_game(id):
    return Game.query.get_or_404(id)


@api.route('/games/', methods=['POST'])
@json
def new_game():
    game = Game().from_json(request.json)
    db.session.add(game)
    db.session.commit()
    return {}, 201, {'Location': game.get_url()}

@api.route('/games/<int:id>', methods=['PUT'])
@json
def edit_game(id):
    game = Game.query.get_or_404(id)
    game.from_json(request.json)
    db.session.add(game)
    db.session.commit()
    return {}

@api.route('/games/<int:id>', methods=['DELETE'])
@json
def delete_game(id):
    game = Game.query.get_or_404(id)
    game.active = False
    db.session.commit()
    return {}
