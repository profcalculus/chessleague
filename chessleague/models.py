from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for, current_app
from .helpers import args_from_url
from .errors import ValidationError

from sqlalchemy import and_, or_
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

import uuid
import hashlib
from ipdb import set_trace as DBG

from chessleague import app
db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='posts')
    date = db.Column(db.Date)
    post = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Post by {} on {}>'.format(self.user, self.date)

    @classmethod
    def get(cls, id=None, user_id=None, date=None):
        query = db.session.query(Post).filter(Post.active)
        if id is not None:
            query = query.filter(Post.id == id)
        else:
            if user_id is not None:
                query = query.filter(Post.user_id == user_id)
            if date is not None:
                query = query.filter(Post.date == date)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(64), index=True)
    #  , unique=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(120))
    #  , unique=True)
    phone1 = db.Column(db.String(15))
    phone2 = db.Column(db.String(15))
    admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', back_populates='contacts')
    posts = db.relationship('Post', back_populates='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])


    @property
    def full_name(self):
        return ("anonymous" if self.is_anonymous
            else "{} ({} {})".format (
                self.user_name, self.first_name, self.last_name))

    def get_url(self):
        return url_for('api.get_user', id=self.id, _external=True)

    def to_json(self):
        return {
        'user_name': self.user_name,
        'first_name': self.first_name,
        'last_name': self.last_name,
        'email': self.email,
        'phone1': self.phone1,
        'phone2': self.phone2,
        'team': self.team.get_url(),
        'admin':self.admin,
        }

    def from_json(self, json):
        for key, value in json.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                app.logger.error('{}: could not set attribute {} to {}'
                    .format(self.__class__.__name__, key, value))
        return self

    @classmethod
    def get(cls, id=None, user_name=None,
            first_name=None, last_name=None, email=None,
            phone1=None, phone2=None, admin=None, team_id=None):
        query = db.session.query(User).filter(User.active)
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
            if phone1 is not None:
                query = query.filter(User.phone1 == phone1)
            if phone2 is not None:
                query = query.filter(User.phone2 == phone2)
            if admin is not None:
                query = query.filter(User.admin == admin)
            if team_id is not None:
                query = query.filter(User.team_id == team_id)
            return query.all()

    @classmethod
    def hash(cls, password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode()
            + password.encode()).hexdigest() + ':'+ salt

    @classmethod
    def check_password(cls, hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode()
            + user_password.encode()).hexdigest()

    @classmethod
    def authenticate(cls, user_name, password):
        """ Authenticates an admin user based on the password.
        If the user is an admin and the password matches the user record
        (after hashing), return a session key (valid until midnight).
        Else return None.
        """
        user = db.session.query(User).filter(user_name == User.user_name).one()
        if user is None or not user.admin:
            return None
        if hash(password) == user.password_hash:
            return SessionKey.add(user)

    @classmethod
    def login (cls, user_name, password):
        today = datetime.now().date()
        # TODO

        #  db.session.execute

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40), index=True)
    dob = db.Column(db.Date)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', back_populates='players')
    active = db.Column(db.Boolean, default=True)

    @property
    def player_id(self):
        return self.id

    def __repr__(self):
        return'<Player {} {}>'.format(self.first_name, self.last_name)

    def get_url(self):
        return url_for('api.get_player', id=self.id, _external=True)

    def to_json(self):
        return {
        'first_name': self.first_name,
        'last_name': self.last_name,
        'dob': self.dob,
        'team': url_for('api.get_team', id=self.team_id, _external=True),
        }

    def from_json(self, json):
        for key, value in json.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                app.logger.error('{}: could not set attribute {} to {}'
                    .format(self.__class__.__name__, key, value))
        return self

    @classmethod
    def get(cls, id=None, first_name=None, last_name=None, dob=None, team_id=None):
        query = db.session.query(Player).filter(Player.active)
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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), index=True)
    contacts = db.relationship('User', back_populates='team', lazy='dynamic')
    players = db.relationship('Player', back_populates='team', lazy='dynamic')
    active = db.Column(db.Boolean, default=True)

    @property
    def team_id(self):
        return self.id

    def __repr__(self):
        return '<Team {}>'.format(self.name)

    def get_url(self):
        return url_for('api.get_team', id=self.id, _external=True)

    def to_json(self):
        return {
        'name': self.name,
        'contacts':
            [url_for('api.get_user', id=c.id, _external=True) for c in self.contacts],
        'players':
            [url_for('api.get_player', id=p.id, _external=True) for p in self.players],
        }

    def from_json(self, json):
        for key, value in json.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                app.logger.error('{}: could not set attribute {} to {}'
                    .format(self.__class__.__name__, key, value))
        return self

    @classmethod
    def get(cls, id=None, name=None):
        query = db.session.query(Team).filter(Team.active)
        if id is not None:
            query = query.filter(Team.id == id)
        else:
            if name is not None:
                query = query.filter(Team.name == name)
        return query.all()

    @property
    def all_matches(self):
        return db.session.query(Match).filter_by(
            or_(team_1_id=self.id, team_2_id=self.id))

class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_1_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team_2_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    date = db.Column(db.Date)
    result_1 = db.Column(db.Integer)  # HALF-points
    result2 = db.Column(db.Integer)  # HALF-points
    active = db.Column(db.Boolean, default=True)


    def get_url(self):
        return url_for('api.get_match',id=self.id, _external=True)

    def to_json(self):
        return {
            'team_1': self.team_1.get_url(),
            'team_2': self.team_2.get_url(),
            'date': self.date,
            'games': [g.get_url() for g in self.games],
            'result': self.result_str(),
        }

    def from_json(self, json):
        for key, value in json.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                app.logger.error('{}: could not set attribute {} to {}'
                    .format(self.__class__.__name__, key, value))
        return self

    def __repr__(self):
            return "<Match {} vs {}, {:%Y/%m/%d} {}>" .format(
                self.team_1.name, self.team_2.name,
                self.date, self.result_str())

    @property
    def teams(self):
        return [self.team_1, self.team_2]

    @classmethod
    def get(cls, id=None, team_1_id=None, team_2_id=None, date=None):
        query = db.session.query(Match).filter(Match.active)
        if id is not None:
            query = query.filter(Match.id == id)
        else:
            # Order of team parameters does not matter
            if team_1_id or team_2_id:
                ids = (team_1_id, team_2_id)
                query = query.filter(or_(Match.team_1_id in ids, Match.team_2_id in ids))
            if date is not None:
                query = query.filter(Match.date == date)
        return query.all()

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
        res2 = self.result() #  An ordered pair of ints - values are doubled
        if res2 is None:
            result = "?-?"
        else:
            for res in res2:
                if res % 2 == 0:
                    res = "{0:d}".format(res/2)
                else:
                    res = "{:0.1f}".format(res/2.0)
            result = "{}-{}".format(res2[0], res2[1])
        return result

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    white_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    black_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    match = db.relationship('Match', back_populates='games')
    # White win, black win, draw, unknown)
    result = db.Column(db.Enum('?','W', 'B', '='))
    defaulted = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    def get_url(self):
        return url_for('api.get_game', id=self.id, _external=True)

    def to_json(self):
        return {
        'white': self.white.get_url(),
        'black': self.black.get_url(),
        'match': self.match.get_url(),
        'result': self.result_str(),
        }

    def from_json(self, json):
        for key, value in json.items():
            try:
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
        return '<Game {} - {} ({})>'.format(
            self.white.full_name, self.black.full_name, self.result)

    @classmethod
    def get(cls, id=None, white_id=None,
        black_id=None, player_id = None, match_id=None):
        query = db.session.query(Game).filter(Game.active)
        if id is not None:
            query = query.filter(Game.id == id)
        else:
            if white_id is not None:
                query = query.filter(white_id == Game.white_id)
            if black_id is not None:
                query = query.filter(black_id == Game.black_id)
            if player_id is not None:
                query = query.filter(player_id in (Game.white_id, Game.black_id))
            if match_id is not None:
                query = query.filter(match_id == Game.match_id)
        return query.all()

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
        self.expiry = today + timedelta(days=1)

    def check(self, user, session_key):
        """ Verify that user holds a current session key.
        Purge expired session keys, then return True iff
        user has a stored session key that matches the key in the request.
        """
        #  Purge old session keys
        db.session.delete(SessionKey).filter(SessionKey.expiry <= datetime.now().date())
        db.session.commit()
        if session_key is None:
            return False
        stored_session_key = db.session.query(SessionKey).filter(
            SessionKey.user_id == user.id).one().session_key
        return session_key == stored_session_key

    @classmethod
    def add(cls, user):
        """ Make a new session key for an admin user.
        Return the session_key value (valid for the current day only).
        """
        assert user.admin
        new_key = SessionKey(user)
        db.session.add(new_key)
        db.session.commit()
        return new_key.session_key


# Add relationships after all model classes are defined

Game.white = db.relationship('Player', foreign_keys="[Game.white_id]")
Game.black = db.relationship('Player', foreign_keys="[Game.black_id]")
Match.team_1 = db.relationship('Team', foreign_keys="[Match.team_1_id]")
Match.team_2 = db.relationship('Team', foreign_keys="[Match.team_2_id]")
Match.games = db.relationship('Game')
