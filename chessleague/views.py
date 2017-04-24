#!/usr/bin/env python
from chessleague import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/chessleague.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
