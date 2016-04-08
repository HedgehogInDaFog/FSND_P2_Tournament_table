-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

CREATE TABLE players (
	pid		integer PRIMARY KEY nextval('serial'),
	name	text
);

CREATE TABLE results (
	gid			integer PRIMARY KEY nextval('serial'),
	tournament	integer,
	player1		integer,
	player2		integer,
	round		integer,
	result		varchar(5)
);

CREATE TABLE tournament_members (
	tid		integer,
	pid		integer
);
