from flask_restful import Resource, fields, marshal_with

from chessleague import app
from chessleague.models import db, User

from chessleague.api import api, bad_request, BaseRequestParser, BASE_URL

USER_FIELDS = {
    'uri': fields.Url('user'),
    'user_name': fields.String(default="Anonymous"),
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone1': fields.String,
    'phone2': fields.String,
    'admin': fields.Boolean(default=False),
    'team_uri': fields.Url('team'),
}

OPTIONAL_PARSER = BaseRequestParser()
OPTIONAL_PARSER.add_argument('user_name', type=str)
OPTIONAL_PARSER.add_argument('first_name', type=str)
OPTIONAL_PARSER.add_argument('last_name', type=str)
OPTIONAL_PARSER.add_argument('email', type=str)
OPTIONAL_PARSER.add_argument('phone1', type=str)
OPTIONAL_PARSER.add_argument('phone2', type=str)
OPTIONAL_PARSER.add_argument('admin', type=bool)

REQUIRED_PARSER = OPTIONAL_PARSER.copy()
REQUIRED_PARSER.add_argument(
    'user_name', type=str, required=True,
    help='No user name supplied', location='json')
REQUIRED_PARSER.add_argument(
    'first_name', type=str, required=True,
    help='No first name supplied', location='json')
REQUIRED_PARSER.add_argument(
    'last_name', type=str, required=True,
    help='No last name supplied', location='json')
REQUIRED_PARSER.add_argument(
    'password', type=str, required=True,
    help='No password supplied', location='json')


class UserAPI(Resource):
    def __init__(self):
        app.logger.debug('UserAPI.__init__')
        super(UserAPI, self).__init__()

    @marshal_with(USER_FIELDS, envelope='user')
    def get(self, id):
        try:
            user = User.get(id=id)[0]
        except Exception as e:
            return bad_request("User not found: %r" % e)
        args = OPTIONAL_PARSER.parse_args()
        for k, v in args.items():
            if v is not None:
                try:
                    setattr(user, k, v)
                except Exception as e:
                    app.logger.error('get() failed: %r' % e)
        return user

    @marshal_with(USER_FIELDS, envelope='user')
    def put(self, id):
        app.logger.debug('user.put()')
        try:
            user = User.get(id=id)[0]
        except Exception as e:
            return bad_request("User not found: %r" % e)
        args = OPTIONAL_PARSER.parse_args()
        for k, v in args.items():
            if v is not None:
                try:
                    setattr(user, k, v)
                except Exception as e:
                    app.logger.error('put() failed: %r' % e)
        db.session.commit()
        return user

    def delete(self, id):
        try:
            user = User.get(id=id)[0]
        except Exception as e:
            return bad_request("User not found: %r" % e)
        user.active = False
        db.session.commit()


class UserListAPI(Resource):
    def __init__(self):
        app.logger.debug('UserListAPI.__init__()')
        super(UserListAPI, self).__init__()

    @marshal_with(USER_FIELDS, envelope='users')
    def get(self):
        app.logger.debug('UserListAPI.get()')
        try:
            args = OPTIONAL_PARSER.parse_args()
            users = User.get(**args)
        except Exception as e:
            app.logger.error("reqparse failed: %r" % e)
            users = []
        return users

    @marshal_with(USER_FIELDS, envelope='users')
    def post(self):
        app.logger.debug('UserListAPI.post()')
        args = REQUIRED_PARSER.parse_args()
        user = User(
            user_name=args['user_name'],
            first_name=args['first_name'],
            last_name=args['last_name'],
            email=args['email'],
            phone1=args['phone1'],
            phone2=args['phone2'],
            admin=args['admin'],
            team_id=args['team_id']
        )
        db.session.add(user)
        db.session.commit()
        users = User.get()
        return users

api.add_resource(UserListAPI, BASE_URL+'/users', endpoint='users')
api.add_resource(UserAPI, BASE_URL+'/users/<int:id>', endpoint='user')
