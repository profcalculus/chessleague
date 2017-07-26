from datetime import datetime

from flask import request, current_app

from chessleague.models import Match, db
from chessleague.decorators import etag, paginate, json
from . import api, API_BASE_URL


@api.route(API_BASE_URL + '/matches/', methods=['GET'])
@etag
# @paginate()
@json
def get_matches():
    return Match.query


@api.route(API_BASE_URL + '/matches/<int:id>', methods=['GET'])
@etag
@json
def get_match(id):
    return Match.query.get_or_404(id)


@api.route(API_BASE_URL + '/matches/<int:id>/teams/', methods=['GET'])
@etag
def get_match_teams(id):
    match = Match.query.get_or_404(id)
    return match.teams


@api.route(API_BASE_URL + '/matches/<int:id>/games/', methods=['GET'])
@etag
@json
def get_match_games(id):
    match = Match.query.get_or_404(id)
    return match.games


@api.route(API_BASE_URL + '/matches/', methods=['POST'])
@json
def new_match():
    match = Match().from_json(request.json)
    db.session.add(match)
    db.session.commit()
    return {}, 201, {'Location': match.get_url()}


@api.route(API_BASE_URL + '/matches/<int:id>', methods=['PUT'])
@json
def edit_match(id):
    match = Match.query.get_or_404(id)
    match.from_json(request.json)
    db.session.add(match)
    db.session.commit()
    return {}, 204
@api.route(API_BASE_URL + '/matches/<int:id>', methods=['DELETE'])
@json
def delete_match(id):
    match = Match.query.get_or_404(id)
    match.deleted = True
    db.session.commit()
    return {}, 204
