from datetime import datetime

from flask import request

from chessleague import app
from chessleague.models import db, Match
from chessleague.decorators import etag, paginate, json
from . import api

@api.route('/matches/', methods=['GET'])
@etag
@paginate()
def get_matches():
    return Match.query

@api.route('/matches/<int:id>', methods=['GET'])
@etag
@json
def get_match(id):
    return Match.query.get_or_404(id)

@api.route('/matches/<int:id>/teams/', methods=['GET'])
@etag
@paginate()
def get_match_teams(id):
    match = Match.query.get_or_404(id)
    return match.teams

@api.route('/matches/', methods=['POST'])
@json
def new_match():
    match = Match().from_json(request.json)
    db.session.add(match)
    db.session.commit()
    return {}, 201, {'Location': match.get_url()}

@api.route('/matches/<int:id>', methods=['PUT'])
@json
def edit_match(id):
    match = Match.query.get_or_404(id)
    match.from_json(request.json)
    db.session.add(match)
    db.session.commit()
    return {}

@api.route('/matches/<int:id>', methods=['DELETE'])
@json
def delete_match(id):
    match = Match.query.get_or_404(id)
    match.active = False
    db.session.commit()
    return {}
