from datetime import datetime

from flask import abort, url_for, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with

from chessleague import app
from chessleague.models import db, User, Player, Game, Match, Team
from base_request_parser import BaseRequestParser
from ipdb import set_trace as BP

api = Api(app)

BASE_URL = app.config['BASE_URL']

PLAYER_FIELDS = {
    'uri': fields.Url('player'),
    'first_name': fields.String,
    'last_name': fields.String,
    'dob': fields.DateTime(dt_format='iso8601'), # YYYY-MM-DD
    'team_uri': fields.Url('team')
}

def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response

class PlayerAPI(Resource):
    def __init__(self):
        self.reqparse = BaseRequestParser()
        self.reqparse.add_argument(
            'first_name', type=str,
            help='No first name supplied', location='json')
        self.reqparse.add_argument(
            'last_name', type=str,
            help='No last name supplied', location='json')
        self.reqparse.add_argument(
            'dob', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), location='json')
        super(PlayerAPI, self).__init__()

    @marshal_with(PLAYER_FIELDS, envelope='player')
    def get(self, id):
        try:
            player = Player.get(id=id)[0]
        except Exception as e:
            return bad_request("Player not found: %r" % e)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                try:
                    setattr(player, k, v)
                except Exception as e:
                    app.logger.error('get() failed: %r' % e)
        return player

    @marshal_with(PLAYER_FIELDS, envelope='player')
    def put(self, id):
        app.logger.debug('put()')
        BP()
        try:
            player = Player.get(id=id)[0]
        except Exception as e:
            return bad_request("Player not found: %r" % e)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                try:
                    setattr(player, k, v)
                except Exception as e:
                    app.logger.error('put() failed: %r' % e)
        db.session.commit()
        return player

    def delete(self, id):
        try:
            player = Player.get(id=id)[0]
        except Exception as e:
            return bad_request("Player not found: %r" % e)
        player.active = False;
        db.session.commit()


class PlayerListAPI(Resource):

    def __init__(self):
        self.reqparse = BaseRequestParser()
        self.reqparse.add_argument(
            'first_name', type=str,
            help='No first name supplied', location='json')
        self.reqparse.add_argument(
            'last_name', type=str,
            help='No last name supplied', location='json')
        self.reqparse.add_argument(
            'dob', type=datetime, default=None, location='json')
        super(PlayerListAPI, self).__init__()

    @marshal_with(PLAYER_FIELDS, envelope='players')
    def get(self):
        app.logger.debug('PlayerListAPI.get()')
        BP()
        try:
            args = self.reqparse.parse_args()
            players = Player.get(**args)
        except Exception as e:
            app.logger.error("reqparse failed: %r" % e)
            players = []
        return players

    @marshal_with(PLAYER_FIELDS, envelope='players')
    def post(self):
        app.logger.debug('PlayerListAPI.post()')
        args = self.reqparse.parse_args()
        player = {
            'first_name': args['first_name'],
            'last_name': args['last_name'],
            'dob': args['dob'],
            'team_id': args['team_id']
        }
        db.session.add(player)
        db.session.commit()
        players = Player.get()
        return players

api.add_resource(PlayerListAPI, BASE_URL+'/players', endpoint='players')
api.add_resource(PlayerAPI, BASE_URL+'/players/<int:id>', endpoint='player')
