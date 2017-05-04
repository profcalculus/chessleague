#chessleague/fixtures/test_fixtures.py

import unittest

from chessleague import app
from chessleague.models import db, User, Player, Game, Team, Match, Post

from flask_fixtures import FixturesMixin

# Configure the app with the testing configuration
app.config.from_object('chessleague.config.TestConfig')


# Make sure to inherit from the FixturesMixin class
class TestLeague(unittest.TestCase, FixturesMixin):

    # Specify the fixtures file(s) you want to load.
    # Change the list below to ['authors.yaml'] if you created your fixtures
    # file using YAML instead of JSON.
    fixtures = ['test.json']

    # Specify the Flask app and db we want to use for this set of tests
    app = app
    db = db

    # Your tests go here

    def test_users(self):
        users = User.query.all()
        assert len(users) == User.query.count() == 4

    def test_matches(self):
        matches = Match.query.all()
        self.assertEqual(len(matches),Match.query.count())
        self.assertEqual(0, len(matches))
        teams = Team.query.all()
        assert teams[0].name=='CapaCrusaders'
        t0 = teams[0]
        p1 = Player('Alexander', 'Alekhine', team=t0)
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(1, len(t0.players.all()))
        p2 = Player.query.filter_by(lastname='Capablanca').first()
        t0.players.append(p2)
        self.assertEqual('Jose', p2.firstname)
        self.assertEqual(2, len(t0.players.all()))
        db.session.commit()


    def test_games(self):
        kasp = Player.query.filter_by(lastname='Kasparov').first()
        karp = Player.query.filter_by(lastname='Karpov').first()
        g = Game(kasp, karp, result='+1')
        db.session.add(g)
        db.session.commit()
        game = Game.query.first()
        self.assertEqual(g,game)
        self.assertEqual(game.white.firstname,'Garry')
        self.assertEqual(game.black.firstname,'Anatoly')

    def test_teams(self):
        teams = Team.query.all()
        karp = Player.query.filter_by(firstname='Anatoly').first()
        kasp = Player.query.filter_by(firstname='Garry').first()
        lask = Player.query.filter_by(firstname='Emanuel').first()
        capa = Player.query.filter_by(firstname='Jose').first()

        teams[0].players.append(karp)
        teams[0].players.append(kasp)
        teams[1].players.append(lask)
        teams[1].players.append(capa)

        db.session.add(teams[0])
        db.session.add(teams[1])
        db.session.commit()
        t0_players = teams[0].players.all()
        t1_players = teams[1].players.all()
        self.assertItemsEqual((karp,kasp), t0_players)
        self.assertItemsEqual((lask,capa), t1_players)





#        m = Match(teams[0],teams[1], datetime(),






