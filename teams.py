""" Crawler the teams from transfermarkt. """
import re
import parser
import crawler


def get_players(team_name, team_id, season):
    """ Get the players from a team.

        Return a dict of players names and ID.
    """
    link = parser.team_detailed_link_assemble(team_name, team_id, season)
    players_page = crawler.get_page(link)

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
    link = parser.team_link_assemble(team_name, team_id, season)
    team_page = crawler.get_page(link)

    team_info = {}

    team_info["Team Name"] = team_name
    team_info["Id"] = team_id
    team_info["Season"] = season

    token = 'class="container-hauptinfo">'
    team_info["Manager"] = parser.retrieve_in_tags(token,
                                                   "</a>", team_page)
    team_info["Manager Id"] = parser.retrieve_in_tags("profil/trainer/",
                                                      '">', team_page)

    team_info["Income"] = parser.retrieve_in_tags('class="greentext rechts">',
                                                  "</td>", team_page)

    team_info['Income'] = parser.remove_tokens(team_info['Income'],
                                               ['\t', '\n'])

    team_info["Expend."] = parser.retrieve_in_tags('class="redtext rechts">',
                                                   "</td>", team_page)[0]

    team_info['Expend.'] = parser.remove_tokens(team_info['Expend.'],
                                                ['\t', '\n'])

    parsed_season = parser.parse_season(season)

    titles_link = parser.titles_link_assemble(team_name, team_id)
    titles_page = crawler.get_page(titles_link)

    titles = parser.retrieve_in_tags("<h2", "<h2>", titles_page, False)

    season_titles = []
    for title in titles:
        if parsed_season in title:
            season_titles.append(parser.retrieve_in_tags(">", "</h2>", title))

    season_titles = list(map(lambda x: re.sub(r'[\d]+x ', '', x),
                             season_titles))
    if not season_titles:
        team_info['Titles'] = None

    return team_info
