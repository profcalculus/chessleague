# chessleague/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config.from_object('chessleague.config')

from chessleague import views, models, api
from chessleague.api import player_api, team_api
