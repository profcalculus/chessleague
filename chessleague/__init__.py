# chessleague/__init__.py
import os

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
import sqlite3

import config

app = Flask(__name__)
app.config.from_object('chessleague.config')

from chessleague import models, api
from chessleague.api import player_api, team_api, user_api

# Debugging
from ipdb import set_trace as BP

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'chessleague.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='charles',
    PASSWORD='charles'
))

app.config.from_envvar('CHESSLEAGUE_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """

    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
