from flask import request

from ..models import Team, Player, User, db
from ..decorators import etag, paginate, json
from . import api, API_BASE_URL


@api.route(API_BASE_URL + '/teams/', methods=['GET'])
@etag
@paginate()
def get_teams():
    q = Team.query
    return q


@api.route(API_BASE_URL + '/teams/<int:id>', methods=['GET'])
@etag
@json
def get_team(id):
    q = Team.query.get_or_404(id)
    return q


@api.route(API_BASE_URL + '/teams/<int:id>/players/', methods=['GET'])
@etag
@json
def get_team_players(id):
    team = Team.query.get_or_404(id)
    return team.players


@api.route(API_BASE_URL + '/teams/<int:id>/contacts/', methods=['GET'])
@etag
@json
def get_team_contacts(id):
    team = Team.query.get_or_404(id)
    return team.contacts


@api.route(API_BASE_URL + '/teams/<int:id>/matches/', methods=['GET'])
@etag
@json
# @paginate()
def get_team_matches(id):
    team = Team.query.get_or_404(id)
    return team.matches


@api.route(API_BASE_URL + '/teams/', methods=['POST'])
@json
def new_team():
    team = Team().from_json(request.json)
    db.session.add(team)
    db.session.commit()
    return {}, 201, {'Location': team.get_url()}


@api.route(API_BASE_URL + '/teams/<int:id>', methods=['PUT'])
@json
def edit_team(id):
    team = Team.query.get_or_404(id)
    team.from_json(request.json)
    db.session.add(team)
    db.session.commit()
    return {}


@api.route(API_BASE_URL + '/teams/<int:id>', methods=['DELETE'])
@json
def delete_team(id):
    team = Team.query.get_or_404(id)
    team.deleted = True
    db.session.commit()
    return {}, 204
