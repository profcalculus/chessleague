#!/usr/bin/env python
import os.path
from migrate.versioning import api

from chessleague.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from chessleague.models import db

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI,
                        SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI,
                        SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        env = sys.argv[1]
    else:
        env = sys.getenv('CHESSLEAGUE_CONFIG', 'development')
    chessleague.config.configure_app
