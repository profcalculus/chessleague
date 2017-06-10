from flask import request, current_app
from chessleague import db
from chessleague.models import Player
from chessleague.decorators import etag, paginate, json, log
from . import api
from pdb import set_trace as DBG

@api.route('/players/', methods=['GET'])
@etag
@paginate()
# @log
def get_players():
    q = Player.query
    return q


@api.route('/players/<int:id>', methods=['GET'])
@etag
@json
def get_player(id):
    q = Player.query.get_or_404(id)
    return q


@api.route('/players/<int:id>/team/', methods=['GET'])
@etag
# @log
def get_player_team(id):
    player = Player.query.get_or_404(id)
    return player.team


@api.route('/players/<int:id>/games/', methods=['GET'])
@etag
@paginate()
def get_player_games(id):
    player = Player.query.get_or_404(id)
    return player.games


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
    return {}, 204


@api.route('/players/<int:id>', methods=['DELETE'])
@json
def delete_player(id):
    player = Player.query.get_or_404(id)
    player.deleted = True
    db.session.commit()
    return {}, 204
