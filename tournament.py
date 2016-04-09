#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

POINTS_FOR_WIN = 1
POINTS_FOR_DRAW = 0
POINTS_FOR_BYE = 1


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()

    c.execute("DELETE FROM Matches;")

    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()

    c.execute("DELETE FROM Players;")
    c.execute("DELETE FROM TournamentMembers;")

    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()

    c.execute("SELECT COUNT(pid) FROM Players;")
    count = c.fetchone()[0]

    conn.commit()
    conn.close()

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()

    c.execute("INSERT INTO Players (name) VALUES (%s)", (name,))
    c.execute('''SELECT max(pid)
                FROM Players
                WHERE name = (%s)
        ''', (name,))
    pid = c.fetchone()[0]

    registerPlayerForTournament(pid)  # player always registers to Default
                                      # tournament with TID=0 to be
                                      # compatible with default tests

    conn.commit()
    conn.close()


def registerPlayerForTournament(pid, tid=0):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()

    c.execute("INSERT INTO TournamentMembers (tid, pid) VALUES (%s , %s)", (tid, pid, ))

    conn.commit()
    conn.close()


def playerStandings(tid=0):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    deletePlayers()
    deleteMatches()

    registerPlayer("Num One")
    registerPlayer("Num Two")

    reportMatch(1, 2)
    reportMatch(3, 1)
    reportMatch(1, 2, True)

    conn = connect()
    c = conn.cursor()

    c.execute('''SELECT pid
                FROM TournamentMembers
                WHERE tid = (%s)''', (tid,))
    member_list = c.fetchall()
    print "member list: "
    print member_list
    print

    c.execute('''SELECT player1, player2, p1points, p2points
                FROM Matches
                WHERE Matches.tournament = (%s)''', (tid,))
    result_list = c.fetchall()
    print "result_list: "
    print result_list
    print

    conn.commit()
    conn.close()


def reportMatch(winner, loser, isDraw=False, tid=0):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()

    if isDraw:
        p1points = POINTS_FOR_DRAW
        p2points = POINTS_FOR_DRAW
    else:
        p1points = POINTS_FOR_WIN
        p1points = 0
    c.execute('''INSERT INTO Matches (player1, player2, player1_win, draw, tournament)
                VALUES ((%s), (%s), (%s), (%s), (%s))''', (winner, loser, p1points, p2points, tid,))

    conn.commit()
    conn.close()

def swissPairings(tid=0):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

'''
deletePlayers()
deleteMatches()

registerPlayer("Num One")
registerPlayer("Num Two")
#registerPlayer("Num Three")
#registerPlayer("Num Four")

reportMatch(1, 2)
reportMatch(3, 1)
#reportMatch(2, 1)
#reportMatch(1, 2, True)
'''
