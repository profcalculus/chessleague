--
-- File generated with SQLiteStudio v3.1.1 on Thu May 4 23:52:40 2017
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: games
DROP TABLE IF EXISTS games;

CREATE TABLE games (
    id        INTEGER     NOT NULL,
    white_id  INTEGER     NOT NULL,
    black_id  INTEGER     NOT NULL,
    match_id  INTEGER,
    result    VARCHAR (1),
    defaulted BOOLEAN,
    active    BOOLEAN,
    PRIMARY KEY (
        id
    ),
    FOREIGN KEY (
        white_id
    )
    REFERENCES players (id),
    FOREIGN KEY (
        black_id
    )
    REFERENCES players (id),
    FOREIGN KEY (
        match_id
    )
    REFERENCES matches (id),
    CHECK (result IN ('?', 'W', 'B', '=') ),
    CHECK (defaulted IN (0, 1) ),
    CHECK (active IN (0, 1) )
);


-- Table: matches
DROP TABLE IF EXISTS matches;

CREATE TABLE matches (
    id       INTEGER NOT NULL,
    team1_id INTEGER NOT NULL,
    team2_id INTEGER NOT NULL,
    date     DATE,
    active   BOOLEAN,
    PRIMARY KEY (
        id
    ),
    FOREIGN KEY (
        team1_id
    )
    REFERENCES teams (id),
    FOREIGN KEY (
        team2_id
    )
    REFERENCES teams (id),
    CHECK (active IN (0, 1) )
);


-- Table: players
DROP TABLE IF EXISTS players;

CREATE TABLE players (
    id         INTEGER      NOT NULL
                            DEFAULT auto,
    first_name VARCHAR (40),
    last_name  VARCHAR (40),
    dob        DATE,
    team_id    INTEGER,
    active     BOOLEAN      DEFAULT (1),
    PRIMARY KEY (
        id
    ),
    FOREIGN KEY (
        team_id
    )
    REFERENCES teams (id),
    CHECK (active IN (0, 1) )
);

INSERT INTO players (
                        id,
                        first_name,
                        last_name,
                        dob,
                        team_id,
                        active
                    )
                    VALUES (
                        1,
                        'Alexander',
                        'Alekhine',
                        '1892-10-24',
                        3,
                        1
                    );

INSERT INTO players (
                        id,
                        first_name,
                        last_name,
                        dob,
                        team_id,
                        active
                    )
                    VALUES (
                        2,
                        'Jose',
                        'Capablanca',
                        '1888-11-19',
                        4,
                        1
                    );

INSERT INTO players (
                        id,
                        first_name,
                        last_name,
                        dob,
                        team_id,
                        active
                    )
                    VALUES (
                        3,
                        'Boris',
                        'Spassky',
                        '1936-04-14',
                        3,
                        1
                    );

INSERT INTO players (
                        id,
                        first_name,
                        last_name,
                        dob,
                        team_id,
                        active
                    )
                    VALUES (
                        4,
                        'Tigran',
                        'Petrosian',
                        '1929-06-17',
                        4,
                        1
                    );

INSERT INTO players (
                        id,
                        first_name,
                        last_name,
                        dob,
                        team_id,
                        active
                    )
                    VALUES (
                        5,
                        'Emanuel',
                        'Lasker',
                        '1868-12-24',
                        3,
                        1
                    );
INSERT INTO players (
id,
first_name,
last_name,
dob,
team_id,
active
)
VALUES (
6,
'Frank',
'Marshall',
'1868-12-24',
2,
1
);
INSERT INTO players (
id,
first_name,
last_name,
dob,
team_id,
active
)
VALUES (
7,
'Aron',
'Nimzowitsch',
'1868-12-24',
2,
1
);
INSERT INTO players (
id,
first_name,
last_name,
dob,
team_id,
active
)
VALUES (
8,
'Geza',
'Marocz',
'1868-12-24',
3,
1
);
INSERT INTO players (
id,
first_name,
last_name,
dob,
team_id,
active
)
VALUES (
9,
'Efim',
'Bogoljubow',
'1868-12-24',
4,
1
);
INSERT INTO players (
id,
first_name,
last_name,
dob,
team_id,
active
)
VALUES (
10,
'Salo',
'Flohr',
'1868-12-24',
3,
1
);


-- Table: posts
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id      INTEGER NOT NULL,
    user_id INTEGER,
    date    DATE,
    post    TEXT,
    active  BOOLEAN,
    PRIMARY KEY (
        id
    ),
    FOREIGN KEY (
        user_id
    )
    REFERENCES users (id),
    CHECK (active IN (0, 1) )
);


-- Table: teams
DROP TABLE IF EXISTS teams;

CREATE TABLE teams (
    id     INTEGER      NOT NULL,
    name   VARCHAR (40),
    active BOOLEAN,
    PRIMARY KEY (
        id
    ),
    CHECK (active IN (0, 1) )
);

INSERT INTO teams (
                      id,
                      name,
                      active
                  )
                  VALUES (
                      1,
                      'Capa Crusaders',
                      1
                  );

INSERT INTO teams (
                      id,
                      name,
                      active
                  )
                  VALUES (
                      2,
                      'Alex Avengers',
                      1
                  );

INSERT INTO teams (
                      id,
                      name,
                      active
                  )
                  VALUES (
                      3,
                      'ChubbyCheckers',
                      1
                  );

INSERT INTO teams (
                      id,
                      name,
                      active
                  )
                  VALUES (
                      4,
                      'Perpetuals',
                      1
                  );

INSERT INTO teams (
                      id,
                      name,
                      active
                  )
                  VALUES (
                      5,
                      'GarryGrinders',
                      1
                  );

INSERT INTO teams (
                      id,
                      name,
                      active
                  )
                  VALUES (
                      6,
                      'Zugszwang',
                      1
                  );


-- Table: users
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id         INTEGER       NOT NULL,
    nick_name  VARCHAR (64),
    first_name VARCHAR (30),
    last_name  VARCHAR (30),
    email      VARCHAR (120),
    admin      BOOLEAN,
    active     BOOLEAN,
    team_id    INTEGER,
    PRIMARY KEY (
        id
    ),
    CHECK (admin IN (0, 1) ),
    CHECK (active IN (0, 1) ),
    FOREIGN KEY (
        team_id
    )
    REFERENCES teams (id)
);


-- Index: ix_users_nick_name
DROP INDEX IF EXISTS ix_users_nick_name;

CREATE INDEX ix_users_nick_name ON users (
    nick_name
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
