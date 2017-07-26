#!/usr/bin/env python

import os
import sys
import chessleague

if __name__ == '__main__':
    if len(sys.argv) > 1:
        environment = sys.argv[1]
    else:
        environment = os.getenv('CHESSLEAGUE_CONFIG', 'development')
    app = chessleague.create_app(environment)
    app.run()
