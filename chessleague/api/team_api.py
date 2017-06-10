from flask import request

from .. import db
from ..models import Team, Player, User
from ..decorators import etag, paginate, json
from . import api
from .. import DBG


@api.route('/teams/', methods=['GET'])
@etag
@paginate()
def get_teams():
    q = Team.query
    return q


@api.route('/teams/<int:id>', methods=['GET'])
@etag
@json
def get_team(id):
    q = Team.query.get_or_404(id)
    return q


@api.route('/teams/<int:id>/players/', methods=['GET'])
@etag
@json
def get_team_players(id):
    team = Team.query.get_or_404(id)
    return team.players


@api.route('/teams/<int:id>/contacts/', methods=['GET'])
@etag
@json
def get_team_contacts(id):
    team = Team.query.get_or_404(id)
    return team.contacts


@api.route('/teams/<int:id>/matches/', methods=['GET'])
@etag
@json
# @paginate()
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
    team.deleted = True
    db.session.commit()
    return {}, 204