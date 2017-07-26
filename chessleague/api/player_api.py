from flask import request, current_app
from chessleague.models import Player, db
from chessleague.decorators import etag, paginate, json, log
from . import api, auth, API_BASE_URL


@api.route(API_BASE_URL + '/players/', methods=['GET'])
@etag
@paginate()
# @log
def get_players():
    q = Player.query
    return q


@api.route(API_BASE_URL + '/players/<int:id>', methods=['GET'])
@etag
@json
# @log
def get_player(id):
    q = Player.query.get_or_404(id)
    return q


@api.route(API_BASE_URL + '/players/<int:id>/team/', methods=['GET'])
@etag
# @log
def get_player_team(id):
    player = Player.query.get_or_404(id)
    return player.team


@api.route(API_BASE_URL + '/players/<int:id>/games/', methods=['GET'])
@etag
@paginate()
def get_player_games(id):
    player = Player.query.get_or_404(id)
    return player.games


@api.route(API_BASE_URL + '/players/', methods=['POST'])
@auth.login_required
@json
def new_player():
    player = Player().from_json(request.json)
    db.session.add(player)
    db.session.commit()
    return {}, 201, {'Location': player.get_url()}


@api.route(API_BASE_URL + '/players/<int:id>', methods=['PUT'])
@auth.login_required
@json
def edit_player(id):
    player = Player.query.get_or_404(id)
    player.from_json(request.json)
    db.session.add(player)
    db.session.commit()
    return {}, 204


@api.route(API_BASE_URL + '/players/<int:id>', methods=['DELETE'])
@auth.login_required
@json
def delete_player(id):
    player = Player.query.get_or_404(id)
    player.deleted = True
    db.session.commit()
    return {}, 204
