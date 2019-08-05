""" Main module of Transfermarket Crawler

    Given a league link, this crawler will get:
        - The teams of each season
        - The players of each team at each season
        - The historic of each player player
"""

import parser
import leagues
import players
import teams

if __name__ == '__main__':

    SEASON_START = 2000
    SEASON_END = 2019

    for league in parser.file_read("Input/leagues.txt").split('\n'):

        league_teams = leagues.get_teams(league)

        for team in league_teams:

            seasons = []  # new list of seasons of a team

            for season in range(SEASON_START, SEASON_END):

                team_players = teams.get_players(league_teams[team],
                                                 team, season)
                players_info = []  # new list of player for each season

                for player in team_players:

                    players_info.append(players.get_player_info(
                                                team_players[player], player))

                seasons.append({season: players_info})

            parser.file_write("Output/teams_output.txt", {team: seasons})
