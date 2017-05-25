from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
matches = Table('matches', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('team_1_id', Integer),
    Column('team_2_id', Integer),
    Column('date', Date),
    Column('result_1', Integer),
    Column('result2', Integer),
    Column('active', Boolean, default=ColumnDefault(True)),
)

users = Table('users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nick_name', VARCHAR(length=64)),
    Column('first_name', VARCHAR(length=30)),
    Column('last_name', VARCHAR(length=30)),
    Column('email', VARCHAR(length=120)),
    Column('admin', BOOLEAN),
    Column('active', BOOLEAN),
    Column('team_id', INTEGER),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_name', String(length=64)),
    Column('first_name', String(length=30)),
    Column('last_name', String(length=30)),
    Column('email', String(length=120)),
    Column('phone1', String(length=15)),
    Column('phone2', String(length=15)),
    Column('admin', Boolean, default=ColumnDefault(False)),
    Column('password_hash', String(length=100)),
    Column('active', Boolean, default=ColumnDefault(True)),
    Column('team_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['matches'].columns['team_1_id'].create()
    post_meta.tables['matches'].columns['team_2_id'].create()
    pre_meta.tables['users'].columns['nick_name'].drop()
    post_meta.tables['users'].columns['password_hash'].create()
    post_meta.tables['users'].columns['phone1'].create()
    post_meta.tables['users'].columns['phone2'].create()
    post_meta.tables['users'].columns['user_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['matches'].columns['team_1_id'].drop()
    post_meta.tables['matches'].columns['team_2_id'].drop()
    pre_meta.tables['users'].columns['nick_name'].create()
    post_meta.tables['users'].columns['password_hash'].drop()
    post_meta.tables['users'].columns['phone1'].drop()
    post_meta.tables['users'].columns['phone2'].drop()
    post_meta.tables['users'].columns['user_name'].drop()
