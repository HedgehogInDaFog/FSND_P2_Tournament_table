-- Table definitions for the tournament project.

DROP DATABASE tournament;
CREATE DATABASE tournament;

\c tournament;

DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS TournamentMembers;
DROP TABLE IF EXISTS Rules;

CREATE TABLE Players (
	pid		serial PRIMARY KEY,
	name	text
);

CREATE TABLE Matches (
	mid			serial PRIMARY KEY,
	player1		integer, -- id of the player
	p1points	integer,
	player2		integer, -- id of the player
	p2points	integer,
	tournament	integer
);

CREATE TABLE TournamentMembers (
	tid		integer,
	pid		integer 
);
