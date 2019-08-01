""" Crawler the leagues from Transfermarkt. """
import re
import parser


def get_league_teams(league_link):
    """ Return all the teams of a given league. """
    league_page = parser.get_page(league_link)

    league_page = parser.cut_page('id="verein_select_breadcrumb"',
                                  "</select>", league_page)

    clubs_id = parser.retrieve_in_tags('value="', '">', league_page)
    clubs_name = parser.retrieve_in_tags('>', '<', league_page)

    clubs_id = parser.remove_token(clubs_id, ['', ' '])
    # letting only digts on the list
    clubs_id = list(filter(lambda x: re.match(r'\d', x), clubs_id))

    clubs_name = parser.remove_token(clubs_name, ['\n', 'Club'])

    return {int(clubs_id[index]): name for index,
            name in enumerate(clubs_name)}
