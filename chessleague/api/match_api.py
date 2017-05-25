from datetime import datetime

from flask_restful import Resource, fields, marshal_with

from chessleague import app
from chessleague.models import db, Match
from chessleague.api import api, bad_request, BaseRequestParser, BASE_URL


MATCH_FIELDS = {
    'uri': fields.Url('match'),
    'name': fields.String(),
    'contact_uris': fields.List(fields.Url('user')),
    'player_uris': fields.List(fields.Url('player')),
}

# Request parser with all fields optional
OPTIONAL_PARSER = BaseRequestParser()
OPTIONAL_PARSER.add_argument(
    'team_1_id', type=int, location='json')
OPTIONAL_PARSER.add_argument(
    'team_2_id', type=int, location='json')
OPTIONAL_PARSER.add_argument(
    'date', type=datetime, location='json')
OPTIONAL_PARSER.add_argument(
    'result', type=str, location='json', default='?')

# Request parser with some fields required
REQUIRED_PARSER = OPTIONAL_PARSER.copy()
REQUIRED_PARSER.add_argument(
    'team_1_id', type=int, required=True,
    help='No id for team 1', location='json')
REQUIRED_PARSER.add_argument(
    'team_2_id', type=int, required=True,
    help='No id for team 2', location='json')


class MatchAPI(Resource):
    def __init__(self):
        super(MatchAPI, self).__init__()

    @marshal_with(MATCH_FIELDS, envelope='match')
    def get(self, id):
        try:
            match = Match.get(id=id)[0]
        except Exception as e:
            return bad_request("Match not found: %r" % e)
        args = OPTIONAL_PARSER.parse_args()
        for k, v in args.items():
            if v is not None:
                try:
                    setattr(match, k, v)
                except Exception as e:
                    app.logger.error('get() failed: %r' % e)
        return match

    @marshal_with(MATCH_FIELDS, envelope='match')
    def put(self, id):
        app.logger.debug('put()')
        try:
            match = Match.get(id=id)[0]
        except Exception as e:
            return bad_request("Match not found: %r" % e)
        args = OPTIONAL_PARSER.parse_args()
        for k, v in args.items():
            if v is not None:
                try:
                    setattr(match, k, v)
                except Exception as e:
                    app.logger.error('put() failed: %r' % e)
        db.session.commit()
        return match

    def delete(self, id):
        try:
            match = Match.get(id=id)[0]
        except Exception as e:
            return bad_request("Match not found: %r" % e)
        match.active = False
        db.session.commit()


class MatchListAPI(Resource):
    def __init__(self):
        super(MatchListAPI, self).__init__()

    @marshal_with(MATCH_FIELDS, envelope='matches')
    def get(self):
        app.logger.debug('MatchListAPI.get()')
        try:
            args = self.reqparse.parse_args()
            matches = Match.get(**args)
        except Exception as e:
            app.logger.error("reqparse failed: %r" % e)
            matches = []
        return matches

    @marshal_with(MATCH_FIELDS, envelope='matches')
    def post(self):
        app.logger.debug('MatchListAPI.post()')
        args = REQUIRED_PARSER.parse_args()
        match = Match(
            team_1_id=args['team_1_id'],
            team_2_id=args['team_2_id'],
            date=args['date'],
        )
        db.session.add(match)
        db.session.commit()
        matches = Match.get()
        return matches

api.add_resource(MatchListAPI, BASE_URL+'/matches', endpoint='matches')
api.add_resource(MatchAPI, BASE_URL+'/matches/<int:id>', endpoint='match')
