from flask import request, jsonify, Blueprint, g

from ..errors import ValidationError, bad_request, not_found
from ..decorators import rate_limit

from ..auth import auth
from .. import app

api = Blueprint('api', __name__)
API_BASE_URL = app.config.get('API_BASE_URL')
# from ..auth import auth


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])


@api.errorhandler(400)
def bad_request_error(e):
    return bad_request('invalid request')


@api.errorhandler(404)
def not_found_error(e):
    return not_found('item not found')


@api.before_request
@rate_limit(limit=5, per=15)
# @auth.login_required
def before_request():
    pass


@api.after_request
def after_request(response):
    READONLY_METHODS = 'GET, HEAD, OPTIONS'
    ALL_METHODS = READONLY_METHODS + ', PUT, DELETE'
    if hasattr(g, 'headers'):
        response.headers.extend(g.headers)
    http_host = request.environ['HTTP_HOST']
    allow_origin = 'http://' + http_host.split(':')[0] + ':4200' #TODO Hacky hacky
    response.headers['Access-Control-Allow-Origin'] = allow_origin
    response.headers['Content-Type'] = 'application/json'
    admin_user=True # TODO: fix this
    response.headers['Access-Control-Allow-Methods'] = (
        ALL_METHODS if admin_user else READONLY_METHODS)
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    app.logger.debug('Response headers: %s' % response.headers)
    return response

@api.route(API_BASE_URL)
def index():
    return '<h3>Chessleague API</h3>'

# do this last to avoid circular dependencies
from . import player_api, user_api, game_api, team_api, match_api
