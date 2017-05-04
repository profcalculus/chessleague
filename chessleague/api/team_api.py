from datetime import datetime

from flask import abort, url_for, jsonify
from flask_restful import Api, Resource, fields, marshal_with

from chessleague import app
from chessleague.models import db, Team

from base_request_parser import BaseRequestParser
from ipdb import set_trace as BP

api = Api(app)

BASE_URL = app.config['BASE_URL']

TEAM_FIELDS = {
    'uri': fields.Url('team'),
    'name': fields.String,
}

def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response

class TeamAPI(Resource):

    def __init__(self):
        app.logger.debug('TeamAPI.__init__')
        self.reqparse = BaseRequestParser()
        self.reqparse.add_argument(
            'name', type=str,
            help='No team name supplied', location='json')
        super(TeamAPI, self).__init__()

    @marshal_with(TEAM_FIELDS, envelope='team')
    def get(self, id):
        try:
            team = Team.get(id=id)[0]
        except:
            return bad_request("Team not found")
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                team[k] = v
        return team

    @marshal_with(TEAM_FIELDS, envelope='team')
    def put(self, id):
        try:
            team = Team.get(id=id)[0]
        except:
            return bad_request("Team not found")
        args = self.reqparse.parse_args()
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
        Team.active = False;
        db.session.commit()

class TeamListAPI(Resource):

    def __init__(self):
        app.logger.debug('TeamListAPI.__init__()')
        self.reqparse = BaseRequestParser()
        self.reqparse.add_argument(
            'name', type=str,
            help='No team name supplied', location='json')
        super(TeamListAPI, self).__init__()

    @marshal_with(TEAM_FIELDS, envelope='teams')
    def get(self):
        app.logger.debug('TeamListAPI.get()')
        try:
            args = self.reqparse.parse_args()
        except:
            pass
        teams = Team.get(**args)
        return teams

    @marshal_with(TEAM_FIELDS, envelope='teams')
    def post(self):
        app.logger.debug('TeamListAPI.post()')
        args = self.reqparse.parse_args()
        team = {
            'name': args['name'],
        }
        db.session.add(team)
        db.session.commit()
        teams = Team.get()
        return teams

api.add_resource(TeamListAPI, BASE_URL+'/teams', endpoint='teams')
api.add_resource(TeamAPI, BASE_URL+'/teams/<int:id>', endpoint='team')
