#!/usr/bin/env python

import os
import sys
import chessleague

if __name__ == '__main__':
    if len(sys.argv) > 1:
        environment = sys.argv[1]
    else:
        environment = os.getenv('CHESSLEAGUE_CONFIG', 'development')
    chessleague.app.config.update(chessleague.config.get_config(environment))
chessleague.app.run(debug=True)
