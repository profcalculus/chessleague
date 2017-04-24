from flask_sqlalchemy import SQLAlchemy
from chessleague import app
db = SQLAlchemy(app)
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True)
    #  , unique=True)
    firstname = db.Column(db.String(30))
    email = db.Column(db.String(120), unique=True)
    phone1 = db.column(db.String(15))
    phone2 = db.column(db.String(15))
    admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, nickname, firstname, lastname,
                 email=None, phone1=None, phone2=None, admin=False):
        self.nickname = nickname
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone1 = phone1
        self.phone2 = phone2
        self.admin = admin

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        admin = '*' if self.admin else ''
        return '<User {}{} ({} {})>'.format(
            admin, self.nickname, self.firstname, self.lastname)


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(40))
    lastname = db.Column(db.String(40))
    dob = db.Column(db.DateTime)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    # games = db.relationship(
    #     'Game', foreign_keys='[games.white_id, games.black_id]',
    #     backref='players', lazy='dynamic')
    active = db.Column(db.Boolean, default=True)

    def __init__(self, firstname, lastname, dob=None, team=None):
        self.firstname = firstname
        self.lastname = lastname
        self.dob = dob
        self.team = team

    def __repr__(self):
        return'<Player {} {}>'.format(self.firstname, self.lastname)


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    contacts = db.relationship('User', backref='team', lazy='dynamic')
    players = db.relationship('Player', backref='team', lazy='dynamic')
    # matches = db.relationship(
    #     'Match', backref="teams", lazy='dynamic')
    active = db.Column(db.Boolean, default=True)

    def __init__(self, name, primary_contact=None):
        self.name = name
        self.contact = primary_contact

    def __repr__(self):
        return '<Team {}>'.format(self.name)


class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team_1 = db.relationship('Team', foreign_keys=[team1_id])
    team_2 = db.relationship('Team', foreign_keys=[team2_id])
    # teams = db.relationship('Team', foreign_keys=[team1_id, team2_id])
    date = db.Column(db.DateTime)
    result1 = db.column(db.Integer)  # HALF-points
    result2 = db.column(db.Integer)  # HALF-points
    games = db.relationship('Game', backref='match', lazy='dynamic')
    active = db.Column(db.Boolean, default=True)

    def __init__(self, team1, team2,
                 date, result1=None, result2=None, games=None):
        self.team1 = team1
        self.team2 = team2
        self.date = date
        self.result1 = result1
        self.result2 = result2
        self.games = games

    def __repr__(self):
            return "<Match {} vs {}, {:%Y/%m/%d} {}>" .format(
                self.team1.name, self.team2.name,
                self.date, self.result_str())

    def result(self):
        """ Computes the match result from the games.
        Returns a tuple (team1_score, team2_score) """
        games = self.games.all()
        if not games:
            return None
        t1 = t2 = 0
        for game in games:
            if game.result:
                if game.result in ('+', 'D'):
                    t1 += 1
                elif game.result in ('-', 'd'):
                    t2 += 1
                else:
                    t1 += 0.5
                    t2 += 0.5
        return (t1, t2)

    def _result_str(self):
        # Sane representation of match result, eg "1.5-2.5"
        res2 = self.result()
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
    id = db.Column(db.Integer, primary_key=True)
    white_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    black_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    white = db.relationship('Player', foreign_keys=[white_id])
    black = db.relationship('Player', foreign_keys=[black_id])
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    # White win, black win, draw, defaults(ifo W/B)
    result = db.Enum(('+', '-', '=', 'D', 'd'))
    active = db.Column(db.Boolean, default=True)

    def __init__(self, white, black, match=None, result=None):
        self.white = white
        self.black = black
        self.match = match
        self.result = result

    def __repr__(self):
        return '<Game {}-{} {}>'.format(
            self.white.lastname, self.black.lastname, self.result)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime)
    post = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, user, post, date=None):
        self.user = user
        self.post = post
        if date is None:
            date = datetime.utcnow()
        self.date = date

    def __repr__(self):
        return '<Post by {} on {}>'.format(self.user, self.date)
