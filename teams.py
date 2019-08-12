""" Crawler the teams from transfermarkt. """
import parser
import crawler


def get_players(team_name, team_id, season):
    """ Get the players from a team.

        Return a dict of players names and ID.
    """
    players_page = _return_page(team_name, team_id, season)

    begin_token = '<a name="zugaenge" class="anchor">'
    end_token = '<div class="werbung werbung-fullsize_contentad">'
    page = parser.cut_page(begin_token, end_token, players_page)

    begin_token = '<td class="hauptlink">'
    pages = parser.retrieve_in_tags(begin_token, '/a>', page, False)

    # inside the pages, we must have a href
    pages = list(filter(lambda x: 'href' in x, pages))

    players_info = {}

    for page in pages:

        player_id = parser.retrieve_in_tags('id="', '"', page)
        player_name = parser.retrieve_in_tags(player_id+'">', '<', page)

        if player_name is not None:
            players_info[player_id] = player_name

    return players_info

def get_team_info(team_name, team_id, season):
    """ Get teams info.

        Returns a dict with all team info
    """
    team_page = _return_page(team_name, team_id, season)

    team_info = {}

    team_info["Team Name"] = team_name
    team_info["Id"] = team_id
    team_info["Season"] = season
    team_info["Manager"] = parser.retrieve_in_tags("Manager:</div>", "</a>",
                                                   team_page)
    team_info["Income"] = parser.retrieve_in_tags('class="greentext rechts">', "</td>",
                                                  team_page)
    team_info["Expenditures"] = parser.retrieve_in_tags('class="redtext rechts">', "</td>",
                                                        team_page)
    team_info['Titles'] = None

    return team_info

def _return_page(team_name, team_id, season):
    """ Return the html from team page. """
    link = parser.team_link_assemble(team_name, team_id, season)

    return crawler.get_page(link)
