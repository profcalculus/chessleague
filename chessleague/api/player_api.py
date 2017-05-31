from flask import request

from chessleague.models import db, Player
from chessleague.decorators import etag, paginate, json
from . import api

@api.route('/players/', methods=['GET'])
@etag
@paginate()
def get_players():
    return Player.query

@api.route('/players/<int:id>', methods=['GET'])
@etag
@json
def get_player(id):
    return Player.query.get_or_404(id)

@api.route('/players/<int:id>/team/', methods=['GET'])
@etag
@paginate()
def get_player_team(id):
    player = Player.query.get_or_404(id)
    return player.team

@api.route('/players/', methods=['POST'])
@json
def new_player():
    player = Player().from_json(request.json)
    db.session.add(player)
    db.session.commit()
    return {}, 201, {'Location': player.get_url()}

@api.route('/players/<int:id>', methods=['PUT'])
@json
def edit_player(id):
    player = Player.query.get_or_404(id)
    player.from_json(request.json)
    db.session.add(player)
    db.session.commit()
    return {}

@api.route('/players/<int:id>', methods=['DELETE'])
@json
def delete_player(id):
    player = Player.query.get_or_404(id)
    player.active = False
    db.session.commit()
    return {}
