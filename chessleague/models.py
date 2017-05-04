from flask_sqlalchemy import SQLAlchemy
from chessleague import app
db = SQLAlchemy(app)
from datetime import datetime
from ipdb import set_trace as debug


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    post = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, user, post, date=None):
        self.user = user
        self.post = post
        if date is None:
            date = datetime.utcnow()
        self.date = date
        self.active = True

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
    nick_name = db.Column(db.String(64), index=True)
    #  , unique=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(120))
    #  , unique=True)
    phone1 = db.column(db.String(15))
    phone2 = db.column(db.String(15))
    admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, nick_name, first_name, last_name,
                 email=None, phone1=None, phone2=None, admin=False):
        self.nick_name = nick_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone1 = phone1
        self.phone2 = phone2
        self.admin = admin
        self.active = True

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
            admin, self.nick_name, self.first_name, self.last_name)

    @classmethod
    def get(cls, id=None, nick_name=None,
            first_name=None, last_name=None, email=None,
            phone1=None, phone2=None, admin=None):
        query = db.session.query(User).filter(User.active)
        if id is not None:
            query = query.filter(User.id == id)
        else:
            if nick_name is not None:
                query = query.filter(User.nick_name == nick_name)
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
            return query.all()


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    dob = db.Column(db.Date)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    active = db.Column(db.Boolean, default=True)

    # games = db.relationship(
    #     'Game', foreign_keys='[games.white_id, games.black_id]',
    #     backref='players', lazy='dynamic')
    def __init__(self, first_name, last_name, dob=None, team_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.team_id = team_id
        self.active = True

    def __repr__(self):
        return'<Player {} {}>'.format(self.first_name, self.last_name)

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
        return query.all()


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    contacts = db.relationship('User', backref='team', lazy='dynamic')
    players = db.relationship('Player', backref='team', lazy='dynamic')
    # matches = db.relationship(
    #     'Match', backref="teams", lazy='dynamic')
    active = db.Column(db.Boolean, default=True)

    def __init__(self, name, contact=None):
        self.name = name
        self.contact = contact
        self.active = True

    def __repr__(self):
        return '<Team {}>'.format(self.name)

    @classmethod
    def get(cls, id=None, name=None):
        query = db.session.query(Team).filter(Team.active)
        if id is not None:
            query = query.filter(Team.id == id)
        else:
            if name is not None:
                query = query.filter(Team.name == name)
        return query.all()


class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    team_1 = db.relationship('Team', foreign_keys=[team1_id])
    team_2 = db.relationship('Team', foreign_keys=[team2_id])
    # teams = db.relationship('Team', foreign_keys=[team1_id, team2_id])
    date = db.Column(db.Date)
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
        self.active = True

    def __repr__(self):
            return "<Match {} vs {}, {:%Y/%m/%d} {}>" .format(
                self.team1.name, self.team2.name,
                self.date, self.result_str())

    @classmethod
    def get(cls, id=None, team1_id=None, team2_id=None, date=None):
        query = db.session.query(Match).filter(Match.active)
        if id is not None:
            query = query.filter(Match.id == id)
        else:
            if team1_id is not None:
                query = query.filter(team1_id in (Match.team1_id, Match.team2_id))
            if team2_id is not None:
                query = query.filter(team2_id in (Match.team1_id, Match.team2_id))
            if date is not None:
                query = query.filter(Match.date == date)
        return query.all()

    def result(self):
        """ Computes the DOUBLED match result from the games as a pair of ints.
        Returns (team1_score*2, team2_score*2) """
        games = self.games.all()
        if not games:
            return None
        res1 = res2 = 0
        for game in games:
            if game.result != '?':
                if game.result == '=':
                    res1 += 1
                    res2 += 1
                else:
                    if game.white in self.team1:
                        if game.result == 'W':
                            res1 += 2
                        else:
                            res2 += 2
                    else:  # game.result == 'B'
                        if game.black in self.team1:
                            res1 += 1
                        else:
                            res2 += 1
        return (res1, res2)

    def _result_str(self):
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
    white = db.relationship('Player', foreign_keys=[white_id])
    black = db.relationship('Player', foreign_keys=[black_id])
    # players = db.relationship('Player', foreign_keys=[white_id, black_id])
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    # White win, black win, draw, unknown)
    result = db.Column(db.Enum('?','W', 'B', '='))
    defaulted = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, white, black, match=None, result=None):
        self.white = white
        self.black = black
        self.match = match
        self.result = result
        self.active = True

    def __repr__(self):
        return '<Game {}-{} {}>'.format(
            self.white.last_name, self.black.last_name, self.result)

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
