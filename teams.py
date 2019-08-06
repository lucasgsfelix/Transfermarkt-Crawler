""" Crawler the teams from transfermarkt. """
import parser


def get_players(team_name, team_id, season):
    """ Get the players from a team.

        Return a dict of players names and ID.
    """
    link = parser.team_link_assemble(team_name, team_id, season)

    players_page = parser.get_page(link)

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
