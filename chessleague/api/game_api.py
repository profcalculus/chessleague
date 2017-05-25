from flask_restful import Resource, fields, marshal_with

from chessleague import app
from chessleague.models import db, Game
from chessleague.api import api, BaseRequestParser, bad_request, BASE_URL


GAME_FIELDS = {
    'uri': fields.Url('game'),
    'white': fields.String(),
    'black': fields.String,
    'match_uru': fields.Url('match'),
    'result': fields.String(default='?'),
    'defaulted': fields.Boolean(default=False),
}

# Request parser with all fields optional
OPTIONAL_PARSER = BaseRequestParser()
OPTIONAL_PARSER.add_argument(
    'white_id', type=int, location='json')
OPTIONAL_PARSER.add_argument(
    'black_id', type=int, location='json')
OPTIONAL_PARSER.add_argument(
    'match_id', type=int, location='json')
OPTIONAL_PARSER.add_argument(
    'result', type=str, location='json', default='?')

# Request parser with some fields required
REQUIRED_PARSER = OPTIONAL_PARSER.copy()
REQUIRED_PARSER.add_argument(
    'white_id', type=int, required=True,
    help='No id for white', location='json')
REQUIRED_PARSER.add_argument(
    'black_id', type=int, required=True,
    help='No id for black', location='json')
REQUIRED_PARSER.add_argument(
    'match_id', type=int, required=True,
    help='No match id supplied', location='json')


class GameAPI(Resource):
    def __init__(self):
        app.logger.debug('GameAPI.__init__()')
        super(GameAPI, self).__init__()

    @marshal_with(GAME_FIELDS, envelope='game')
    def get(self, id):
        try:
            game = Game.get(id=id)[0]
        except Exception as e:
            return bad_request("Game not found: %r" % e)
        args = OPTIONAL_PARSER.parse_args()
        for k, v in args.items():
            if v is not None:
                try:
                    setattr(game, k, v)
                except Exception as e:
                    app.logger.error('get() failed: %r' % e)
        return game

    @marshal_with(GAME_FIELDS, envelope='game')
    def put(self, id):
        app.logger.debug('put()')
        try:
            game = Game.get(id=id)[0]
        except Exception as e:
            return bad_request("Game not found: %r" % e)
        args = OPTIONAL_PARSER.parse_args()
        for k, v in args.items():
            if v is not None:
                try:
                    setattr(game, k, v)
                except Exception as e:
                    app.logger.error('put() failed: %r' % e)
        db.session.commit()
        return game

    def delete(self, id):
        try:
            game = Game.get(id=id)[0]
        except Exception as e:
            return bad_request("Game not found: %r" % e)
        game.active = False
        db.session.commit()


class GameListAPI(Resource):
    def __init__(self):
        super(GameListAPI, self).__init__()

    @marshal_with(GAME_FIELDS, envelope='games')
    def get(self):
        app.logger.debug('GameListAPI.get()')
        try:
            args = OPTIONAL_PARSER.parse_args()
            games = Game.get(**args)
        except Exception as e:
            app.logger.error("reqparse failed: %r" % e)
            games = []
        return games

    @marshal_with(GAME_FIELDS, envelope='games')
    def post(self):
        app.logger.debug('GameListAPI.post()')
        reqparse = REQUIRED_PARSER.copy()
        args = reqparse.parse_args()
        game = Game(
            white_id=args['white_id'],
            black_id=args['black_id'],
            match_id=args['match_id'],
            result=args['result'],
            defaulted=args['defaulted']
        )
        db.session.add(game)
        db.session.commit()
        games = Game.get()
        return games

api.add_resource(GameListAPI, BASE_URL+'/games', endpoint='games')
api.add_resource(GameAPI, BASE_URL+'/games/<int:id>', endpoint='game')
