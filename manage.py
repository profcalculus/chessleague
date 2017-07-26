#!/usr/bin/env python

from flask_script import Manager, Command
from chessleague import create_app

app = create_app('development')
manager = Manager(app)

@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)

if __name__ == '__main__':
    manager.run()
