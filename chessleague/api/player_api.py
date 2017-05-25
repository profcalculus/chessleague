from datetime import datetime

from flask_restful import Resource, fields, marshal_with

from chessleague import app
from chessleague.models import db, Player
from chessleague.api import api, BaseRequestParser, bad_request, BASE_URL

PLAYER_FIELDS = {
    'uri': fields.Url('player'),
    'first_name': fields.String,
    'last_name': fields.String,
    'dob': fields.DateTime(dt_format='iso8601'),  # YYYY-MM-DD
    'team_uri': fields.Url('team')
}

# Request parser with all fields optional
OPTIONAL_PARSER = BaseRequestParser()
OPTIONAL_PARSER.add_argument(
    'first_name', type=str, location='json')
OPTIONAL_PARSER.add_argument(
    'last_name', type=str, location='json')
OPTIONAL_PARSER.add_argument(
    'dob', type=lambda x: datetime.strptime(x, '%Y-%m-%d'), location='json')
OPTIONAL_PARSER.add_argument('team', type=int, location='json')

# Request parser with some fields required
REQUIRED_PARSER = OPTIONAL_PARSER.copy()
REQUIRED_PARSER.add_argument(
    'first_name', type=str, required=True,
    help='No first name supplied', location='json')
REQUIRED_PARSER.add_argument(
    'last_name', type=str, required=True,
    help='No last name supplied', location='json')


class PlayerAPI(Resource):
    def __init__(self):
        super(PlayerAPI, self).__init__()
        self.reqparse = OPTIONAL_PARSER.copy()

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
        player.active = False
        db.session.commit()


class PlayerListAPI(Resource):

    def __init__(self):
        self.reqparse = OPTIONAL_PARSER.copy()
        super(PlayerListAPI, self).__init__()

    @marshal_with(PLAYER_FIELDS, envelope='players')
    def get(self):
        app.logger.debug('PlayerListAPI.get()')
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
        reqparse = REQUIRED_PARSER.copy()
        args = reqparse.parse_args()
        player = Player(
            first_name=args['first_name'],
            last_name=args['last_name'],
            dob=args['dob'],
            team=args['team']
        )
        db.session.add(player)
        db.session.commit()
        players = Player.get()
        return players

api.add_resource(PlayerListAPI, BASE_URL + '/players', endpoint='players')
api.add_resource(PlayerAPI, BASE_URL + '/players/<int:id>', endpoint='player')
