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

    team_info["Manager"] = parser.retrieve_in_tags("Manager:</div>",
                                                   "</a>", team_page)

    team_info["Income"] = parser.retrieve_in_tags('class="greentext rechts">',
                                                  "</td>", team_page)

    team_info['Income'] = parser.remove_tokens(team_info['Income'],
                                               ['\t', '\n'])

    team_info["Expend."] = parser.retrieve_in_tags('class="redtext rechts">',
                                                   "</td>", team_page)[0]

    team_info['Expend.'] = parser.remove_tokens(team_info['Expenditures'],
                                                ['\t', '\n'])

    parsed_season = parser.parse_season(season)

    titles_link = parser.titles_link_assemble(team_name, team_id)
    titles_page = crawler.get_page(titles_link)

    titles = parser.retrieve_in_tags("<h2", "<h2>", titles_page, False)

    season_titles = []
    for title in titles:
        if parsed_season in title:
            season_titles.append(parser.retrieve_in_tags(">", "</h2>", title))

    team_info['Titles'] = season_titles
    # TODO: remove the 8x, 12x, of each title

    return team_info


def _return_page(team_name, team_id, season):
    """ Return the html from team page. """
    link = parser.team_link_assemble(team_name, team_id, season)

    return crawler.get_page(link)
