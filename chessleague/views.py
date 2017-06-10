from flask import render_template
from chessleague import app


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title="ChessLeague")
