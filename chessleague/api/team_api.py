from flask import request

from .. import app
from ..models import db, Team
from ..decorators import etag, paginate, json
from chessleague.api import api

@api.route('/teams/', methods=['GET'])
@etag
@paginate()
def get_teams():
    return Team.query

@api.route('/teams/<int:id>', methods=['GET'])
@etag
@json
def get_team(id):
    return Team.query.get_or_404(id)

@api.route('/teams/<int:id>/players/', methods=['GET'])
@etag
@paginate()
def get_team_players(id):
    team = Team.query.get_or_404(id)
    return team.players

@api.route('/teams/<int:id>/matches/', methods=['GET'])
@etag
@paginate()
def get_team_matches(id):
    team = Team.query.get_or_404(id)
    return team.matches

@api.route('/teams/', methods=['POST'])
@json
def new_team():
    team = Team().from_json(request.json)
    db.session.add(team)
    db.session.commit()
    return {}, 201, {'Location': team.get_url()}

@api.route('/teams/<int:id>', methods=['PUT'])
@json
def edit_team(id):
    team = Team.query.get_or_404(id)
    team.from_json(request.json)
    db.session.add(team)
    db.session.commit()
    return {}

@api.route('/teams/<int:id>', methods=['DELETE'])
@json
def delete_team(id):
    team = Team.query.get_or_404(id)
    team.active = False
    db.session.commit()
    return {}
