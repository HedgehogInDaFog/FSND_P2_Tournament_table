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
	mid			serial PRIMARY KEY,
	player1		integer,
	player2		integer,
	result		varchar(1), -- "W", "D" or "L" for win, draw and lose of first player
	tournament	integer
);

CREATE TABLE tournament_members (
	tid		integer,
	pid		integer,
	number_of_byes	integer DEFAULT 0
);
