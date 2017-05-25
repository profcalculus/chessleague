from flask_restful import Resource, fields, marshal_with

from chessleague import app
from chessleague.models import db, Team
from chessleague.api import api, BaseRequestParser, bad_request, BASE_URL

TEAM_FIELDS = {
    'uri': fields.Url('team'),
    'name': fields.String,
    'players': fields.List(fields.Url('player'))
}

OPTIONAL_PARSER = BaseRequestParser()
OPTIONAL_PARSER.add_argument('name', type=str)
REQUIRED_PARSER = BaseRequestParser()
REQUIRED_PARSER.add_argument(
    'name', type=str, required=True,
    help='No team name supplied', location='json')


class TeamAPI(Resource):

    def __init__(self):
        app.logger.debug('TeamAPI.__init__')
        super(TeamAPI, self).__init__()

    @marshal_with(TEAM_FIELDS, envelope='team')
    def get(self, id):
        try:
            team = Team.get(id=id)[0]
        except:
            return bad_request("Team not found")
        args = OPTIONAL_PARSER.parse_args()
        for k, v in args.items():
            if v is not None:
                team[k] = v
        return team

    @marshal_with(TEAM_FIELDS, envelope='team')
    def put(self, id):
        app.logger.debug('team.put()')
        try:
            team = Team.get(id=id)[0]
        except Exception as e:
            return bad_request("Team not found: %r" % e)
        args = OPTIONAL_PARSER.parse_args()
        for k, v in args.items():
            if v is not None:
                team[k] = v
        db.session.commit()
        return team

    def delete(self, id):
        try:
            team = Team.get(id=id)[0]
        except:
            return bad_request("Team not found")
        team.active = False
        db.session.commit()


class TeamListAPI(Resource):

    def __init__(self):
        app.logger.debug('TeamListAPI.__init__()')
        super(TeamListAPI, self).__init__()

    @marshal_with(TEAM_FIELDS, envelope='teams')
    def get(self):
        args = OPTIONAL_PARSER.parse_args()
        teams = Team.get(**args)
        return teams

    @marshal_with(TEAM_FIELDS, envelope='teams')
    def post(self):
        app.logger.debug('TeamListAPI.post()')
        args = REQUIRED_PARSER.parse_args()
        team = {
            'name': args['name'],
        }
        db.session.add(team)
        db.session.commit()
        teams = Team.get()
        return teams

api.add_resource(TeamListAPI, BASE_URL+'/teams', endpoint='teams')
api.add_resource(TeamAPI, BASE_URL+'/teams/<int:id>', endpoint='team')
