PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

drop table if exists migrate_version;
CREATE TABLE migrate_version (
	repository_id VARCHAR(250) NOT NULL, 
	repository_path TEXT, 
	version INTEGER, 
	PRIMARY KEY (repository_id)
);
INSERT INTO "migrate_version" VALUES('database repository','/home/charles/projects/sandbox/chessleague/chessleague/db_repository',1);

drop table if exists teams;
CREATE TABLE teams (
	id INTEGER NOT NULL, 
	name VARCHAR(40), 
	deleted BOOLEAN default(0), 
	PRIMARY KEY (id), 
	CHECK (deleted IN (0, 1))
);

INSERT INTO "teams" VALUES(1,'Capa Crusaders',0);
INSERT INTO "teams" VALUES(2,'Alex Avengers',0);
INSERT INTO "teams" VALUES(3,'ChubbyCheckers',0);
INSERT INTO "teams" VALUES(4,'Perpetuals',0);
INSERT INTO "teams" VALUES(5,'GarryGrinders',0);
INSERT INTO "teams" VALUES(6,'Zugszwang',0);
INSERT INTO "teams" VALUES(7,'team1',NULL);
INSERT INTO "teams" VALUES(8,'team2',0);
INSERT INTO "teams" VALUES(9,'team3',0);
INSERT INTO "teams" VALUES(10,'team4',0);
INSERT INTO "teams" VALUES(11,'team5',0);
INSERT INTO "teams" VALUES(12,'team6',0);
INSERT INTO "teams" VALUES(13,'team7',0);
INSERT INTO "teams" VALUES(14,'team8',0);
INSERT INTO "teams" VALUES(15,'team9',0);
INSERT INTO "teams" VALUES(16,'team10',0);

drop table if exists users;
CREATE TABLE users (
	id INTEGER NOT NULL, 
	user_name VARCHAR(64) NOT NULL, 
	first_name VARCHAR(30), 
	last_name VARCHAR(30), 
	email VARCHAR(120), 
	phone_1 VARCHAR(15), 
	phone_2 VARCHAR(15), 
	password_hash VARCHAR(100) NOT NULL, 
	team_id INTEGER, 
	deleted BOOLEAN default(0), 
	PRIMARY KEY (id), 
	CHECK (deleted IN (0, 1)), 
	FOREIGN KEY(team_id) REFERENCES teams (id)
);

INSERT INTO "users" VALUES(1,'user1','User1_first','User1_last','user1@users.com',NULL,NULL,'pwd',3,0);
INSERT INTO "users" VALUES(2,'user2','User2_first','User2_last','user2@users.com',NULL,NULL,'pwd',4,0);
INSERT INTO "users" VALUES(3,'user3','User3_first','User3_last','user3@users.com',NULL,NULL,'pwd',1,0);
INSERT INTO "users" VALUES(4,'admin1','Admin1_first','Admin1_last','admin1@users.com',NULL,NULL,'pwd',15,0);
INSERT INTO "users" VALUES(5,'admin2', 'Admin2_first','Admin2_last','admin2@users.com',NULL,NULL,'pwd',5,0);

drop table if exists matches;
CREATE TABLE matches (
	id INTEGER NOT NULL, 
	team_1_id INTEGER, 
	team_2_id INTEGER, 
	date DATE, 
	location VARCHAR(40), 
	result_1 INTEGER, 
	result_2 INTEGER, 
	deleted BOOLEAN default(0), 
	PRIMARY KEY (id), 
	FOREIGN KEY(team_1_id) REFERENCES teams (id), 
	FOREIGN KEY(team_2_id) REFERENCES teams (id), 
	CHECK (deleted IN (0, 1))
);

INSERT INTO "matches" VALUES(1,3,4,'2017-04-01','',NULL,NULL,0);
INSERT INTO "matches" VALUES(2,4,3,'2017-04-02','',NULL,NULL,0);
INSERT INTO "matches" VALUES(3,1,3,'2017-04-03','',NULL,NULL,0);
INSERT INTO "matches" VALUES(4,1,4,'2017-04-04','',NULL,NULL,0);
INSERT INTO "matches" VALUES(5,3,4,'2017-04-04','',NULL,NULL,0);
INSERT INTO "matches" VALUES(6,4,1,'2017-04-05','',NULL,NULL,0);
INSERT INTO "matches" VALUES(7,5,2,'2017-04-06','',NULL,NULL,0);
INSERT INTO "matches" VALUES(8,5,3,'2017-04-06','',NULL,NULL,0);
INSERT INTO "matches" VALUES(9,3,1,'2017-04-06','',NULL,NULL,0);
INSERT INTO "matches" VALUES(10,5,4,'2017-04-07','',NULL,NULL,0);
INSERT INTO "matches" VALUES(11,2,3,'2017-04-07','',NULL,NULL,0);

drop table if exists players;
CREATE TABLE players (
	id INTEGER NOT NULL, 
	first_name VARCHAR(40), 
	last_name VARCHAR(40), 
	dob DATE, 
	email VARCHAR(120), 
	phone_1 VARCHAR(15), 
	phone_2 VARCHAR(15), 
	team_id INTEGER, 
	deleted BOOLEAN default(0), 
	PRIMARY KEY (id), 
	FOREIGN KEY(team_id) REFERENCES teams (id), 
	CHECK (deleted IN (0, 1))
);
INSERT INTO "players" VALUES(1,'Alexander','Alekhine','1892-10-24',5,0);
INSERT INTO "players" VALUES(2,'Jose','Capablanca','1888-11-19',4,0);
INSERT INTO "players" VALUES(3,'Boris','Spassky','1936-04-14',5,0);
INSERT INTO "players" VALUES(4,'Tigran','Petrosian','1929-06-17',2,0);
INSERT INTO "players" VALUES(6,'Emanuel','Lasker','1868-12-24',3,0);
INSERT INTO "players" VALUES(7,'first1','last1','2010-01-01',3,0);
INSERT INTO "players" VALUES(8,'first2','last2','2010-02-01',2,0);
INSERT INTO "players" VALUES(9,'first3','last3','2010-03-01',3,0);
INSERT INTO "players" VALUES(10,'first4','last4','2010-04-01',2,0);
INSERT INTO "players" VALUES(11,'first5','last5','2010-05-01',3,0);
INSERT INTO "players" VALUES(12,'first6','last6','2010-06-01',2,0);
INSERT INTO "players" VALUES(13,'first7','last7','2010-07-01',3,0);
INSERT INTO "players" VALUES(14,'first8','last8','2010-08-01',4,0);
INSERT INTO "players" VALUES(15,'first9','last9','2010-09-01',5,0);
INSERT INTO "players" VALUES(16,'first10','last10','2010-10-01',4,0);

drop table if exists posts;
CREATE TABLE posts (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	date DATE, 
	post TEXT, 
	deleted BOOLEAN default(0), 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	CHECK (deleted IN (0, 1))
);

drop table if exists session_keys;
CREATE TABLE session_keys (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	session_key VARCHAR(40) NOT NULL, 
	expiry DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	UNIQUE (session_key)
);

drop table if exists games;
CREATE TABLE games (
	id INTEGER NOT NULL, 
	white_id INTEGER NOT NULL, 
	black_id INTEGER NOT NULL, 
	match_id INTEGER, 
	result VARCHAR(1), 
	defaulted BOOLEAN default(0), 
	date DATE, 
	deleted BOOLEAN default(0), 
	PRIMARY KEY (id), 
	FOREIGN KEY(white_id) REFERENCES players (id), 
	FOREIGN KEY(black_id) REFERENCES players (id), 
	FOREIGN KEY(match_id) REFERENCES matches (id), 
	CHECK (result IN ('?', 'W', 'B', '=')), 
	CHECK (defaulted IN (0, 1)), 
	CHECK (deleted IN (0, 1))
);
CREATE INDEX ix_teams_name ON teams (name);
CREATE INDEX ix_users_user_name ON users (user_name);
CREATE INDEX ix_players_last_name ON players (last_name);
CREATE UNIQUE INDEX ix_session_keys_user_id ON session_keys (user_id);
CREATE INDEX ix_session_keys_expiry ON session_keys (expiry);
