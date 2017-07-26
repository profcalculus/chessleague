from datetime import date, datetime, timedelta
import uuid
import hashlib
import re
import json

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy, BaseQuery

from .errors import ValidationError

from chessleague import app

db = SQLAlchemy(app)


def parse_date(yyyy_mm_dd):
    try:
        yyyy, mm, dd = [int(comp) for comp in re.split(r'[/\-. ]', yyyy_mm_dd)]
        return date(yyyy, mm, dd)
    except Exception, exc:
        app.logger.error("Cannot parse date '%s'" % yyyy_mm_dd)
        raise ValidationError(exc)


class QueryWithSoftDelete(BaseQuery):
    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=False) if not with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),
                              session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is not None and not getattr(
            obj, 'deleted', False) else None


class User(db.Model):
    __tablename__ = 'users'
    query_class = QueryWithSoftDelete
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(64), nullable=False, index=True)
    #  , unique=True)
    first_name = db.Column(db.String(30), default='')
    last_name = db.Column(db.String(30), default='')
    email = db.Column(db.String(254))
    #  , unique=True)
    phone_1 = db.Column(db.String(15))
    phone_2 = db.Column(db.String(15))
    admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(100), nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', back_populates='contacts')
    posts = db.relationship('Post', back_populates='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @property
    def name(self):
        return ' '.join((self.first_name, self.last_name))

    @property
    def full_name(self):
        return ("{} ({} {})".format(
            self.user_name, self.first_name, self.last_name))

    def get_url(self):
        return url_for('api.get_user', id=self.id, _external=True)

    def to_json(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'name': self.name,
            'email': self.email,
            'phone_1': self.phone_1,
            'phone_2': self.phone_2,
            'team': (self.team.name, self.team.id) if self.team else None,
            'admin': self.admin,
        }

    def from_json(self, json_dict):
        for key, value in json_dict.items():
            try:
                if key == 'password':
                    key = 'password_hash'
                    value = self.hash(value)
                setattr(self, key, value)
            except AttributeError:
                app.logger.error(
                    '{}: could not set attribute {} to {}'
                    .format(self.__class__.__name__, key, value))
        return self

    def __repr__(self):
        return json.dumps(self.to_json())

    @classmethod
    def get(cls, id=None, user_name=None,
            first_name=None, last_name=None, email=None,
            phone_1=None, phone_2=None, admin=None, team_id=None):
        query = db.session.query(User)
        if id is not None:
            query = query.filter(User.id == id)
        else:
            if user_name is not None:
                query = query.filter(User.user_name == user_name)
            if first_name is not None:
                query = query.filter(User.first_name == first_name)
            if last_name is not None:
                query = query.filter(User.last_name == last_name)
            if email is not None:
                query = query.filter(User.email == email)
            if phone_1 is not None:
                query = query.filter(User.phone_1 == phone_1)
            if phone_2 is not None:
                query = query.filter(User.phone_2 == phone_2)
            if admin is not None:
                query = query.filter(User.admin == admin)
            if team_id is not None:
                query = query.filter(User.team_id == team_id)
            return query.all_or_404()

    @classmethod
    def hash(cls, password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(
            salt.encode() + password.encode()).hexdigest() + ':' + salt

    @classmethod
    def authenticate(cls, user_name, password):
        """ Authenticates an admin user based on the password.
        If the password matches the user record
        (after hashing), return a session key (valid until midnight).
        Else return None.
        """
        user = db.session.query(User).filter(user_name == User.user_name).one()
        if user is None:
            return None
        if check_password_hash(user.password_hash, password):
            return SessionKey.add(user)

    @classmethod
    def login(cls, user_name, password):
        today = datetime.now().date()
        # TODO

    @classmethod
    def verify_auth_token(user_name, token):
        return SessionKey.check(user_name, token)

        #  db.session.execute


class Player(db.Model):
    __tablename__ = 'players'
    query_class = QueryWithSoftDelete
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40), index=True)
    dob = db.Column(db.Date)
    email = db.Column(db.String(254))
    phone_1 = db.Column(db.String(15))
    phone_2 = db.Column(db.String(15))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', back_populates='players')
    deleted = db.Column(db.Boolean, default=False)

    @property
    def name(self):
        return ' '.join((self.first_name, self.last_name))

    def __repr__(self):
        return json.dumps(self.to_json())

    def get_url(self):
        return url_for('api.get_player', id=self.id, _external=True)

    def to_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dob': self.dob.isoformat() if self.dob else None,
            'email': self.email,
            'phone_1': self.phone_1,
            'phone_2': self.phone_2,
            'team': {
                'name': self.team.name if self.team else None,
                'id': self.team.id if self.team else None,
            }
        }

    def from_json(self, json_dict):
        for key, value in json_dict.items():
            try:
                if key == 'team':
                    key='team_id'
                    value = json_dict['team']['id']
                elif key == 'dob':
                    value = parse_date(value)
                setattr(self, key, value)
            except AttributeError:
                app.logger.error(
                    '%s: could not set attribute %s to %s'
                    % (self.__class__.__name__, key, value))
                raise ValidationError
        return self

    @property
    def games(self):
        query = db.session.query(Game).filter_by(
            or_(white_id=self.id, black_id=self.id)
            .order_by(Game.date))
        return query.all_or_404()

    @classmethod
    def get(cls, id=None, first_name=None, last_name=None, dob=None, team_id=None):
        query = db.session.query(Player)
        if id is not None:
            query = query.filter(Player.id == id)
        else:
            if first_name is not None:
                query = query.filter(Player.first_name == first_name)
            if last_name is not None:
                query = query.filter(Player.last_name == last_name)
            if dob is not None:
                query = query.filter(Player.dob == dob)
            if team_id is not None:
                query = query.filter(Player.team_id == team_id)
        return query.all_or_404()


class Team(db.Model):
    __tablename__ = 'teams'
    query_class = QueryWithSoftDelete
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), index=True)
    contacts = db.relationship('User', lazy='dynamic', back_populates='team')
    players = db.relationship('Player', lazy='dynamic', back_populates='team')
    deleted = db.Column(db.Boolean, default=False)

    @property
    def team_id(self):
        return self.id

    def __repr__(self):
        return json.dumps(self.to_json())

    def get_url(self):
        return url_for('api.get_team', id=self.id, _external=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'contacts': [{'name': contact.name, 'id': contact.id} for contact in self.contacts],
            'players': [{'name': player.name, 'id': player.id} for player in self.players],
        }

    def from_json(self, json_dict):
        for key, value in json_dict.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                app.logger.error(
                    '{}: could not set attribute {} to {}'
                    .format(self.__class__.__name__, key, value))
        return self

    @classmethod
    def get(cls, id=None, name=None):
        query = db.session.query(Team)
        if id is not None:
            query = query.filter(Team.id == id)
        else:
            if name is not None:
                query = query.filter(Team.name == name)
        return query.all_or_404()

    @property
    def matches(self):
        return db.session.query(Match).filter(
            or_(Match.team_1_id == self.id, Match.team_2_id == self.id)
            .order_by(Match.date))


class Match(db.Model):
    __tablename__ = 'matches'
    query_class = QueryWithSoftDelete
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_1_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team_2_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    date = db.Column(db.Date)
    location = db.Column(db.String(40))
    result_1 = db.Column(db.Integer)  # HALF-points
    result_2 = db.Column(db.Integer)  # HALF-points
    deleted = db.Column(db.Boolean, default=False)

    def get_url(self):
        return url_for('api.get_match', id=self.id, _external=True)

    def to_json(self):
        return {
            'id': self.id,
            'team_1':{'name': self.team_1.name, 'id': self.team_1.id },
            'team_2':{'name': self.team_2.name, 'id': self.team_2.id },
            'date': self.date.isoformat() if self.date else None,
            'games': [{
                'id': game.id,
                'white': {
                    'id': game.white.id,
                    'last_name': game.white.last_name,
                },
                'black': {
                    'id': game.black.id,
                    'last_name': game.black.last_name,
                },
                'result': game.result
            } for game in self.games],
            'result': self.result_str()
        }

    def from_json(self, json_dict):
        for key, value in json_dict.items():
            if key.name == 'date':
                key.value = parse_date(key.value)
            try:
                setattr(self, key, value)
            except AttributeError:
                app.logger.error(
                    '{}: could not set attribute {} to {}'
                    .format(self.__class__.__name__, key, value))
        return self

    def __repr__(self):
        return json.dumps(self.to_json())

    @property
    def teams(self):
        return [self.team_1, self.team_2]

    @classmethod
    def get(cls, id=None, team_1_id=None, team_2_id=None, date=None):
        query = db.session.query(Match)
        if id is not None:
            query = query.filter(Match.id == id)
        else:
            # Order of teams does not matter
            if team_1_id or team_2_id:
                ids = (team_1_id, team_2_id)
                query = query.filter(
                    or_(Match.team_1_id in ids, Match.team_2_id in ids))
            if date is not None:
                query = query.filter(Match.date == date)
        return query.all_or_404()

    def result(self):
        """ Computes the DOUBLED match result from the games as a pair of ints.
        Returns (team_1_score*2, team_2_score*2) """
        res1 = res2 = 0
        for game in self.games:
            if game.result != '?':
                if game.result == '=':
                    res1 += 1
                    res2 += 1
                else:
                    if game.white in self.team_1:
                        if game.result == 'W':
                            res1 += 2
                        else:
                            res2 += 2
                    else:  # game.result == 'B'
                        if game.black in self.team_1:
                            res1 += 1
                        else:
                            res2 += 1
        return (res1, res2)

    def result_str(self):
        # Sane representation of match result, eg "1.5-2.5"
        res2 = self.result()  # An ordered pair of ints - values are doubled
        if res2 is None:
            result = "?-?"
        else:
            for res in res2:
                if res % 2 == 0:
                    res = "{0:d}".format(res / 2)
                else:
                    res = "{:0.1f}".format(res / 2.0)
            result = "{}-{}".format(res2[0], res2[1])
        return result


class Game(db.Model):
    __tablename__ = 'games'
    query_class = QueryWithSoftDelete
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    white_id = db.Column(db.Integer, db.ForeignKey(
        'players.id'), nullable=False)
    black_id = db.Column(db.Integer, db.ForeignKey(
        'players.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    match = db.relationship('Match', back_populates='games')
    # White win, black win, draw, unknown)
    result = db.Column(db.Enum('?', 'W', 'B', '='))
    defaulted = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date)
    deleted = db.Column(db.Boolean, default=False)

    def get_url(self):
        return url_for('api.get_game', id=self.id, _external=True)

    def to_json(self):
        return {
            'id': self.id,
            'white': {
                'id': self.white.id,
                'last_name': self.white.last_name,
            },
            'black': {
                'id': self.black.id,
                'last_name': self.black.last_name,
            },
            'result': self.result_str(),
            'match': {
                'id': self.match.id,
                'team_1': {
                    'id': self.match.team_1.id,
                    'name': self.match.team_1.name
                },
                'team_2': {
                    'id': self.match.team_2.id,
                    'name': self.match.team_2.name
                },
                'result': self.match.result
            }
        }

    def from_json(self, json_dict):
        for key, value in json_dict.items():
            try:
                if key == 'date':
                    value = parse_date(value)
                setattr(self, key, value)
            except AttributeError:
                app.logger.error('{}: could not set attribute {} to {}'
                                 .format(self.__class__.__name__, key, value))
        return self

    def result_str(self):
        result_map = {
            'W': '1-0',
            'B': '0-1',
            '=': '=',
            '?': '?'
        }
        res = result_map[self.result]
        if self.defaulted:
            res += 'D'
        return res

    def __repr__(self):
        return json.dumps(self.to_json())

    @classmethod
    def get(cls, id=None, white_id=None,
            black_id=None, player_id=None, match_id=None):
        query = db.session.query(Game)
        if id is not None:
            query = query.filter(Game.id == id)
        else:
            if white_id is not None:
                query = query.filter(white_id == Game.white_id)
            if black_id is not None:
                query = query.filter(black_id == Game.black_id)
            if player_id is not None:
                query = query.filter(player_id in (
                    Game.white_id, Game.black_id))
            if match_id is not None:
                query = query.filter(match_id == Game.match_id)
        return query.all_or_404()

    @property
    def players(self):
        return [self.white, self.black]


class SessionKey(db.Model):
    __tablename__ = 'session_keys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), unique=True, nullable=False, index=True)
    session_key = db.Column(db.String(40), unique=True, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False, index=True)

    def __init__(self, user):
        self.user_id = user.id
        today = datetime.now().date()
        self.session_key = hash(user.username, today)
        self.expiry = today + timedelta(hours=1)

    @classmethod
    def check(cls, user, session_key):
        """ Verify that user holds a current session key.
        Purge expired session keys, then return True iff
        user has a stored session key that matches the key in the request.
        """
        #  Purge old session keys
        db.session.query(SessionKey).filter(
            SessionKey.expiry >= datetime.now().date()).delete()
        db.session.commit()
        if session_key is None:
            return False
        try:
            stored_session_key = db.session.query(SessionKey).filter_by(
                user_id=user.id).one().session_key
            return session_key == stored_session_key
        except:
            return False

    @classmethod
    def add(cls, user):
        """ Make a new session key for an admin user.
        Return the session_key value (valid for the current day only).
        """
        # assert user.admin
        new_key = SessionKey(user)
        db.session.add(new_key)
        db.session.commit()
        return new_key.session_key


class Post(db.Model):  # Not currently used
    __tablename__ = 'posts'
    query_class = QueryWithSoftDelete
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='posts')
    date = db.Column(db.Date)
    post = db.Column(db.Text)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Post by {} on {}>'.format(self.user, self.date)

    @classmethod
    def get(cls, id=None, user_id=None, pdate=None):
        query = db.session.query(Post)
        if id is not None:
            query = query.filter(Post.id == id)
        else:
            if user_id is not None:
                query = query.filter(Post.user_id == user_id)
            if date is not None:
                query = query.filter(Post.date == pdate)
        return query.all_or_404()

# Add relationships after all model classes are defined


Game.white = db.relationship('Player', foreign_keys="[Game.white_id]")
Game.black = db.relationship('Player', foreign_keys="[Game.black_id]")
Match.team_1 = db.relationship('Team', foreign_keys="[Match.team_1_id]")
Match.team_2 = db.relationship('Team', foreign_keys="[Match.team_2_id]")
Match.games = db.relationship('Game')
