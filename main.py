""" Main module of Transfermarket Crawler

    Given a league link, this crawler will get:
        - The teams of each season
        - The players of each team at each season
        - The historic of each player player
"""

import parser
import leagues


if __name__ == '__main__':

    SEASON_START = 2000
    SEASON_END = 2019

    for league in parser.file_read("Input/leagues.txt").split('\n'):
        teams = leagues.get_league_teams(league)

    for season in range(SEASON_START, SEASON_END):
        pass
