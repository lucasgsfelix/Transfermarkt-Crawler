""" Crawler the teams from transfermarkt. """
import parser
import re


def get_players(team_name, team_id, season):
    """ Get the players from a team.

        Return a dict of players names and ID.
    """
    link = parser.team_link_assemble(team_name, team_id, season)
    print(link)
    page = parser.get_page(link)

    page = parser.cut_page('selected="selected">Player',
                           "</select></div>", page)

    players_id = parser.retrieve_in_tags('value="', '">', page)
    players_name = parser.retrieve_in_tags('>', '<', page)

    players_id = list(filter(lambda x: re.match(r'\d', x), players_id))
    players_name = parser.remove_token(players_name, ['\n'])
    players_name = list(map(lambda x: re.sub(r'^[0-9()]*', '', x),
                            players_name))
    print(players_name)
    exit()

    return {int(players_id[index]): name for index,
            name in enumerate(players_name)}
