-- Table definitions for the tournament project.

DROP DATABASE tournament;
CREATE DATABASE tournament;

\c tournament;

DROP TABLE IF EXISTS Players CASCADE;
DROP TABLE IF EXISTS Matches CASCADE;
DROP TABLE IF EXISTS TournamentMembers CASCADE;

CREATE TABLE Players (
	pid		serial PRIMARY KEY,
	name	text
);

CREATE TABLE TournamentMembers (
	tid		integer,
	pid		integer REFERENCES Players (pid),
	PRIMARY KEY (tid, pid)
);

CREATE TABLE Matches (
	mid			serial PRIMARY KEY,
	player1		integer REFERENCES Players (pid), -- id of the player
	p1points	integer,
	player2		integer REFERENCES Players (pid), -- id of the player
	p2points	integer,
	tournament	integer
);
