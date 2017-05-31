# chessleague/__init__.py
import os

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import sqlite3

from ipdb import set_trace as DBG


app = Flask('chessleague')
app.config.from_object('chessleague.config')
DBG()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

from chessleague import models, api
from chessleague.api import player_api, team_api, user_api, game_api, match_api

# Debugging
from ipdb import set_trace as DBG

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app.config.environment[config_name])

    # if not app.config['DEBUG'] and not app.config['TESTING']:
        # configure logging for production

        # # email errors to the administrators
        # if app.config.get('MAIL_ERROR_RECIPIENT') is not None:
        #     import logging
        #     from logging.handlers import SMTPHandler
        #     credentials = None
        #     secure = None
        #     if app.config.get('MAIL_USERNAME') is not None:
        #         credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        #         if app.config['MAIL_USE_TLS'] is not None:
        #             secure = ()
        #     mail_handler = SMTPHandler(
        #         mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        #         fromaddr=app.config['MAIL_DEFAULT_SENDER'],
        #         toaddrs=[app.config['MAIL_ERROR_RECIPIENT']],
        #         subject='[Talks] Application Error',
        #         credentials=credentials,
        #         secure=secure)
        #     mail_handler.setLevel(logging.ERROR)
        #     app.logger.addHandler(mail_handler)

        # send standard logs to syslog
    import logging
    from logging.handlers import SysLogHandler
    syslog_handler = SysLogHandler()
    syslog_handler.setLevel(logging.WARNING)
    app.logger.addHandler(syslog_handler)

    # bootstrap.init_app(app)
    db = get_db()
    db.init_app(app)
    login_manager.init_app(app)
    return app


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
