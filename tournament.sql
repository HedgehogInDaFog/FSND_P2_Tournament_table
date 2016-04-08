-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

DROP TABLE IF EXISTS players, matches, tournament_members;

CREATE TABLE players (
	pid		serial PRIMARY KEY,
	name	text
);

CREATE TABLE matches (
	gid			serial PRIMARY KEY,
	tournament	integer,
	player1		integer,
	player2		integer,
	result		varchar(5)
);

CREATE TABLE tournament_members (
	tid		integer,
	pid		integer
);