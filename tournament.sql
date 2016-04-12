-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE tournament;
CREATE DATABASE tournament;

\c tournament;

DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS TournamentMembers;

CREATE TABLE Players (
	pid		serial PRIMARY KEY,
	name	text
);

CREATE TABLE Matches (
	mid			serial PRIMARY KEY,
	player1		integer,
	player2		integer,
	result		varchar(1), -- "W" for win, "D" for draw
	tournament	integer
);

CREATE TABLE Points (
	player		integer,
	points		integer,
	tournament	integer
);

CREATE TABLE TournamentMembers (
	tid				integer,
	pid				integer
);
