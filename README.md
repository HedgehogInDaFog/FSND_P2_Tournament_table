# FSND_P2_Tournament_table
Project 2 for Udacity Nanodegree

## Description

This is a database to store the matches between players and a Python module to rank the players and pair them up in matches in a tournaments
Pairing is made for a Swiss tournament

## Environment

To successfully use DB and Python module you need to use:
  - Python 2.7
  - PostgreSQL 9.3

## Files and their brief description
1. tournament.sql - contains DB schema
2. tournament.py - python functions to rank and pair players
3. tournament_test.py - contains a number of tests to check main functionality

## DB Schema

DB Contains three tables:
  - Players
  - TournamentMembers
  - Matches

### Table "Players"
Contains data about players (name, id):

```
 Column |  Type   |                       Modifiers
--------+---------+-------------------------------------------------------
 pid    | integer | not null default nextval('players_pid_seq'::regclass)
 name   | text    |
Indexes:
    "players_pkey" PRIMARY KEY, btree (pid)
```

### Table "Tournament members"
Contains data, about in which tournaments do players participate. 
Player can participate in multiply tournaments
```
    Column    |  Type   | Modifiers
--------------+---------+-----------
 tid          | integer |
 pid          | integer |
 numberofbyes | integer | default 0
```

### Table "Matches"
Contains data about results of the games (matches). 
This is shared table for all tournaments (so it contains results of games for all tournaments)
```
   Column   |         Type         |                       Modifiers
------------+----------------------+-------------------------------------------------------
 mid        | integer              | not null default nextval('matches_mid_seq'::regclass)
 player1    | integer              |
 player2    | integer              |
 result     | character varying(1) |
 tournament | integer              |
Indexes:
    "matches_pkey" PRIMARY KEY, btree (mid)
```

## Python Functions

Detailed description you can find on the commentaries in the code, but the most important functions are:

1. Function to register new players
```
def registerPlayer(name, tid=0):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).
      tid: tournament ID (0 is default tournament)
    """
```

2. Function to see current player standing (ranking)
```
def playerStandings(tid=0):
    """Returns a list of the players and their point records, sorted by points

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Args:
      tid: tournament ID (0 is default tournament)

    Returns:
      A list of tuples, each of which contains (id, name, points, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        points: the number of points, which player earned.
        matches: the number of matches the player has played
    """
```

3. Function to pair players for the next round
```
def swissPairings(tid=0):
    """Returns a list of pairs of players for the next round of a match.

    Each player appears no more than once in the pairings. Each player is
    paired with another player with an equal or nearly-equal points record,
    that is, a player adjacent to him or her in the standings. In case of
    odd number - one player will not be paired

    Args:
      tid: tournament ID (0 is default tournament)

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
```

4. Function to report results of the match
```
def reportMatch(winner, loser, isDraw=False, tid=0):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won/tied
      loser:  the id number of the player who lost/tied
      isDraw: True in case of draw (tie) (False by default to be
        compatible with default tests)
      tid: tournament ID (0 is default tournament)
    """
```

## Contact information

Author: Vladmir Vorotnikov

E-mail: v.s.vorotnikov@gmail.com

Feel free to contact me.