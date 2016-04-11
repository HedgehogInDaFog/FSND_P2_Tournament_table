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
    c.execute("DELETE FROM Points;")

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
    """TODO: description
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

    conn = connect()
    c = conn.cursor()

    c.execute('''SELECT pointsSummary.player, players.name, pointsSummary.points, pointsSummary.matches FROM
                Players, (
                SELECT player, sum(points) AS points, count(player) AS matches
                FROM Points
                WHERE Points.tournament = (%s)
                GROUP BY player
                ) AS pointsSummary
                WHERE pointsSummary.player = Players.pid
                ORDER BY pointsSummary.points DESC
                ''', (tid,))
    result_list = c.fetchall() #full standing without players with zero games

    c.execute('''SELECT TournamentMembers.pid, Players.name
                FROM TournamentMembers, Players
                WHERE TournamentMembers.tid = (%s)
                AND TournamentMembers.pid = Players.pid
        ''', (tid,))

    members_list = c.fetchall() #full list of players in the tournament

    if len(members_list) != len(result_list):
        pid_list = []
        for i in result_list:
            pid_list.append(i[0]) # list of pids in standing  without players with zero games
        for i in members_list:
            if i[0] not in pid_list:
                result_list.append((i[0], i[1], 0, 0)) #add players with zero games

    conn.commit()
    conn.close()

    return result_list

def reportMatch(winner, loser, isDraw=False, tid=0):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()

    if isDraw:
        result = "D"
        c.execute('''INSERT INTO Points (player, points, tournament)
                VALUES ((%s), (%s), (%s))''', (winner, POINTS_FOR_DRAW, tid,))
        c.execute('''INSERT INTO Points (player, points, tournament)
                VALUES ((%s), (%s), (%s))''', (loser, POINTS_FOR_DRAW, tid,))
    else:
        result = "W"
        c.execute('''INSERT INTO Points (player, points, tournament)
                VALUES ((%s), (%s), (%s))''', (winner, POINTS_FOR_WIN, tid,))
        c.execute('''INSERT INTO Points (player, points, tournament)
                VALUES ((%s), (%s), (%s))''', (loser, 0, tid,))

    c.execute('''INSERT INTO Matches (player1, player2, result, tournament)
                VALUES ((%s), (%s), (%s), (%s))''', (winner, loser, result, tid,))

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
    def findPair(standing, pairs, index):
        '''
        finds best pair for person standing[index]
        returns pair index
        '''
        numOfPlayers = len(standing)
        if numOfPlayers < 2:
            return -1
        print "index = " + str(index)
        print
        print str(pairs)
        for i in range(1,len(standing)):
            print i
            if index + i < numOfPlayers:
                if (standing[index][0], standing[index+i][0]) not in pairs and (standing[index+i][0], standing[index][0]) not in pairs:
                    print "return from findPair: " + str(index+i)
                    print
                    return index + i
            if index - i >= 0:
                if (standing[index][0], standing[index-i][0]) not in pairs and (standing[index-i][0], standing[index][0]) not in pairs:
                    print "return from findPair: " + str(index-i)
                    print
                    return index - i

        if index + 1 == numOfPlayers:
            return index - 1
        else:
            return index + 1

    def checkLowNumOfMatches(standing, max):
        '''
        checks, is there any team with number of matches lower then max
        if any - returns first's index
        '''
        print "CheckLow (max): " + str(max)
        print
        for i in range(len(standing)):
            if standing[i][3] < max:
                return i
        return -1

    standing = playerStandings(tid)
    print "Standings: " + str(standing)
    print

    conn = connect()
    c = conn.cursor()

    c.execute('''SELECT player1, player2
                FROM Matches
                WHERE tournament = (%s)''', (tid,))

    pairs = c.fetchall()
    print "Pairs: " + str(pairs)
    print

    final_pairs = []

    #check, if any players with lower number of matches. If exists - find pair for him
    maxMatches = 0
    for i in standing:
        if i[3] > maxMatches:
            maxMatches - i[3]

    while len(standing) > 1:
        print "=======new cycle======"
        print "standings: " + str(standing)
        print
        low = checkLowNumOfMatches(standing, maxMatches)
        if low == -1:
            pair = findPair(standing, pairs, 0)
            print "pair: " + str(pair)
            print
            final_pairs.append((standing[0][0], standing[0][1], standing[pair][0], standing[pair][1]))
            standing.pop(pair)
            standing.pop(0)
        else:
            pair = findPair(standing, pairs, low)
            print "pair low: " + str(pair)
            print
            final_pairs.append((standing[low][0], standing[low][1], standing[pair][0], standing[pair][1]))
            standing.pop(max(low,pair))
            standing.pop(min(low,pair))

    conn.commit()
    conn.close()

    print "Final_pairs: " + str(final_pairs)
    print

    return final_pairs
'''
deletePlayers()
deleteMatches()

registerPlayer("Num One")
registerPlayer("Num Two")
registerPlayer("Num Three")
#registerPlayer("Num Four")

reportMatch(1, 2)
reportMatch(1, 2)
reportMatch(1, 2)
reportMatch(3, 1)
reportMatch(2, 1)
reportMatch(1, 2, True)
'''