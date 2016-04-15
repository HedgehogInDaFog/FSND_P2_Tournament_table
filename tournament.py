#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

POINTS_FOR_WIN = 1   # Such default configuration is done to be compatible
POINTS_FOR_DRAW = 0  # with default tests. It is more interesting to have 3
POINTS_FOR_BYE = 1   # points for win and 1 point for draw


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


def registerPlayer(name, tid=0):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).
      tid: tournament ID (0 is default tournament)
    """
    conn = connect()
    c = conn.cursor()

    c.execute("INSERT INTO Players (name) VALUES (%s)", (name,))
    c.execute('''SELECT max(pid)
                FROM Players
                WHERE name = (%s)
        ''', (name,))
    pid = c.fetchone()[0]

    # registerPlayerForTournament is to support multiply tournaments. One
    # player can participate in any number of tournaments. All players are
    # registered for TID=0 by default to be compartible with default tests
    registerPlayerForTournament(pid, tid)

    conn.commit()
    conn.close()


def registerPlayerForTournament(pid, tid=0):
    """TODO: description
    """
    conn = connect()
    c = conn.cursor()

    c.execute("""INSERT INTO TournamentMembers (tid, pid)
                VALUES (%s , %s)""", (tid, pid, ))

    conn.commit()
    conn.close()


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

    conn = connect()
    c = conn.cursor()

    c.execute('''SELECT ps.player_id, Players.name, ps.points, ps.matches
                FROM Players,
                    (
                        SELECT player_id,
                                sum(points) as points,
                                sum(matches) as matches
                        FROM
                            (
                                SELECT player1 AS player_id,
                                        sum(p1points) AS points,
                                        count(player1) AS matches
                                FROM Matches
                                WHERE Matches.tournament = (%s)
                                GROUP BY player_id

                                UNION

                                SELECT player2 AS player_id,
                                        sum(p2points) AS points,
                                        count(player2) AS matches
                                FROM Matches
                                WHERE Matches.tournament = (%s)
                                GROUP BY player_id
                            ) AS tmp
                        GROUP BY player_id
                    ) AS ps
                WHERE ps.player_id = Players.pid
                ORDER BY ps.points DESC;
            ''', (tid, tid, ))
    result_list = c.fetchall()  # standing without players with 0 games

    c.execute('''SELECT TournamentMembers.pid, Players.name
                FROM TournamentMembers, Players
                WHERE TournamentMembers.tid = (%s)
                AND TournamentMembers.pid = Players.pid
        ''', (tid,))

    members_list = c.fetchall()  # full list of players,
                                 # registered in the tournament
    conn.commit()
    conn.close()

    # Now we need to merge result_list and members_list to get full standings,
    # including those players who has zero games

    # if some members are not in current standing
    # (so if we have any members with zero games)
    if len(members_list) != len(result_list):
        pid_list = []
        for i in result_list:
            pid_list.append(i[0])
        for i in members_list:
            if i[0] not in pid_list:
                result_list.append((i[0], i[1], 0, 0))  # add players
                                                        # with 0 games

    return result_list


def playerStandingsWithBye(tid=0):
    """Returns a list of the players and their point records, sorted by
        points, including points for "Bye" (skipped rounds)

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Args:
      tid: tournament ID (0 is default tournament)

    Returns:
      A list of tuples, each of which contains (id, name, points, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        points: the number of points, which player earned.
        matches: the number of matches the player has played
    """
    ps = playerStandings(tid)  # get standings without Byes
    result = []

    # find maximum number of matches (usually number of rounds)
    maxMatches = 0
    for i in ps:
        if i[3] > maxMatches:
            maxMatches = i[3]

    # find maximum number of matches (usually number of rounds)
    for i in ps:
        if i[3] == maxMatches:  # if player played in all rounds
            result.append(i)    # do not modify original standings
        else:
            # add points for every skipped round:
            addBye = (maxMatches - i[3]) * POINTS_FOR_BYE
            # add modified player information to standings:
            result.append((i[0], i[1], i[2] + addBye, i[3]))
    return result


def reportMatch(winner, loser, isDraw=False, tid=0):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won/tied
      loser:  the id number of the player who lost/tied
      isDraw: True in case of draw (tie) (False by default to be
        compatible with default tests)
      tid: tournament ID (0 is default tournament)
    """

    conn = connect()
    c = conn.cursor()

    if isDraw:
        p1points = POINTS_FOR_DRAW
        p2points = POINTS_FOR_DRAW
    else:
        p1points = POINTS_FOR_WIN
        p2points = 0

    c.execute('''INSERT INTO Matches (player1, p1points, player2,
                                        p2points, tournament)
             VALUES ((%s), (%s), (%s), (%s), (%s))''',
             (winner, p1points, loser, p2points, tid,))

    conn.commit()
    conn.close()


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
    def findPair(standing, pairs, index):
        """
        Finds pair for person standing[index]. Returns index of his best pair

        Args:
          standing: tournament table, containing unpaired playerStandings
          pairs: list of tuples with id's of players who previously played
                against each other
          index: position of player in standing for whom the pair is searching

        Returns:
          index of the player, who is the best pair
        """
        numOfPlayers = len(standing)
        if numOfPlayers < 2:
            return -1

        for i in range(1, len(standing)):
            curr = standing[index][0]
            prev = standing[index-i][0]
            next = standing[index+i][0]
            # check that we are still in the boundaries of our standing:
            if index + i < numOfPlayers:
                # check that this players didn't play against
                # each other previously:
                if (curr, next) not in pairs and (next, curr) not in pairs:
                    return index + i
            # check that we are still in the boundaries of our standing:
            if index - i >= 0:
                # check that this players didn't play against
                # each other previously:
                if (curr, prev) not in pairs and (prev, curr) not in pairs:
                    return index - i

        # in case player previously played with all possible partners,
        # we choose simply adjacent
        if index + 1 == numOfPlayers:
            return index - 1
        else:
            return index + 1

    def checkLowNumOfMatches(standing, max):
        '''
        Checks, is there any player with number of matches lower then
        maximum number of matches any of players has played. It is needed to
        ensure, that those players, who skipped round, will be paired first.
        So nobody will skip round twice, until all skip round at least once.

        Args:
          standing: tournament table, containing unpaired playerStandings
          max: logically - current number of played rounds in the tournament.
            In fact - the maximum number of matches, any of players has played

        Returns:
          index of the first player, who played less than maximum
        '''
        for i in range(len(standing)):
            if standing[i][3] < max:
                return i
        return -1

    standing = playerStandings(tid)

    conn = connect()
    c = conn.cursor()

    c.execute('''SELECT player1, player2
                FROM Matches
                WHERE tournament = (%s)''', (tid,))

    pairs = c.fetchall()  # get previously played matches for better pairing

    final_pairs = []

    # Check, if any players with lower number of matches.
    # If exists - find pair for him first
    maxMatches = 0
    for i in standing:
        if i[3] > maxMatches:
            maxMatches = i[3]

    while len(standing) > 1:
        low = checkLowNumOfMatches(standing, maxMatches)
        if low == -1:  # if there is no player with number matches lower
            low = 0    # than other, than sstart with the first player
        pair = findPair(standing, pairs, low)
        final_pairs.append((standing[low][0], standing[low][1],
                            standing[pair][0], standing[pair][1]))
        standing.pop(max(low, pair))  # remove paired players from temporary
        standing.pop(min(low, pair))  # standing to avoid double-pairing

    conn.commit()
    conn.close()

    return final_pairs
