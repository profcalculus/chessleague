# chessleague/__init__.py
import os

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# import sqlite3

from chessleague import config

# Debugging
from ipdb import set_trace as DBG

app = None
db = None  # The database, initialised in create_app()


def create_app(config_name):
    app = Flask(__name__)
    app.config.update(config.get_config(config_name))
    # if app.config['USE_TOKEN_AUTH']:
    #     from api.token import token as token_blueprint
    #     app.register_blueprint(token_blueprint, url_prefix='/auth')
    import logging
    from logging.handlers import SysLogHandler
    syslog_handler = SysLogHandler()
    syslog_handler.setLevel(logging.WARNING)
    app.logger.addHandler(syslog_handler)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    global db
    db = SQLAlchemy(app)
    db.init_app(app)
    from .models import User,Player,Game,Match,Team,Post
    db.create_all()
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/chessleague')
    return app


if __name__ == '__main__':
    app = create_app(os.getenv('CHESSLEAGUE_CONFIG', 'development'))
