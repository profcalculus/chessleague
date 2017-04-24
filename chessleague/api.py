from flask.ext.restful import Api, Resource, reqparse
from datetime import datetime
from chessleague import app
from chessleague.models import User, Player, Game, Match, Team


api = Api(app)


class PlayerAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'firstname', type=str, required=True,
            help='No first name supplied', location='json')
        self.reqparse.add_argument(
            'lastname', type=str, required=True,
            help='No last name supplied', location='json')
        self.reqparse.add_argument(
            'dob', type=datetime, default=None, location='json')
    def get(self, id):
        player = Player.query.filter(id=id).first()
        #  player = filter(lambda p: p['id'] == id, players)
        if player is None:
            abort(404)
        # player = player[0]
        args = self.reqparse.parse_args()
        for k, v in args.iteritems():
            if v is not None:
                player[k] = v
        return  { 'player': make_public_player(player) }

        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


class PlayerListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'firstname', type=str, required=True,
            help='No first name supplied', location='json')
        self.reqparse.add_argument(
            'lastname', type=str, required=True,
            help='No last name supplied', location='json')
        self.reqparse.add_argument(
            'dob', type=datetime, default=None, location='json')

    def get(self):
        pass

    def post(self):
        pass

api.add_resource(PlayerAPI, '/players/<int:id>', endpoint='player')
api.add_resource(PlayerListAPI, '/players/', endpoint='players')
