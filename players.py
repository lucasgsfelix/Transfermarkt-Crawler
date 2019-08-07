""" Crawler the players from Transfermarkt. """
import time
import parser
from collections import OrderedDict


def get_player_info(player_name, player_id):
    """ Get the information about a player. """

    link = parser.player_link_assemble(player_name, player_id)
    player_page = parser.get_page(link)

    if not player_page:
        time.sleep(60*5)
        player_page = parser.get_page(link)

    player_info = {}

    player_info['Transfers'] = get_player_transfer(player_page)

    player_info['Name'] = player_name.replace('-', ' ').capitalize()

    player_info['Id'] = player_id

    player_info['Full Name'] = parser.retrieve_in_tags("Full Name:</th>",
                                                       "</td>", player_page)

    player_info['Birth Date'] = parser.retrieve_in_tags("Date of Birth:",
                                                        "</a>", player_page)
    span = '</span>'
    player_info['Birth Place'] = parser.retrieve_in_tags('"birthPlace">',
                                                         span, player_page)
    token = 'itemprop="nationality">'
    player_info['Nationality'] = parser.retrieve_in_tags(token,
                                                         span, player_page)

    player_info['Age'] = parser.retrieve_in_tags("Age:</th>", "</td>",
                                                 player_page)

    player_info['Height'] = parser.retrieve_in_tags('itemprop="height"',
                                                    span, player_page)

    player_info['Position(s)'] = parser.retrieve_in_tags("Position:</span>",
                                                         "</p>", player_page)

    player_info['Foot'] = parser.retrieve_in_tags("Foot:",
                                                  "</td>", player_page)

    player_info['Agent'] = parser.retrieve_in_tags("Player Agents:",
                                                   "</a>", player_page)

    player_info['Joined'] = parser.retrieve_in_tags("Joined:</span>",
                                                    span, player_page)
    token = "Contract until:</span>"
    player_info['Contract Length'] = parser.retrieve_in_tags(token,
                                                             span, player_page)

    player_info['Outfiter'] = parser.retrieve_in_tags("Outfitter:",
                                                      "</td>", player_page)

    return player_info


def get_player_transfer(player_page):
    """ Get the transfers made along a player career. """
    player_page = parser.cut_page('<div class="box transferhistorie">',
                                  "</tfoot>", player_page)

    pages = parser.retrieve_in_tags('<tr class="zeile-transfer">', '</tr>',
                                    player_page, False)

    transfers = []
    for page in pages:
        info = {}
        info['Season'] = parser.retrieve_in_tags(
            'class="zentriert hide-for-small"', '</td>', page)[0]
        info['Fee'] = parser.retrieve_in_tags('zelle-abloese', '<', page)
        info['Market Value'] = parser.retrieve_in_tags('zelle-mw', '<', page)
        clubs_name = parser.retrieve_in_tags('vereinsname', '</a>', page)

        # make a set without sorting the list
        clubs_id = list(OrderedDict.fromkeys(parser.retrieve_in_tags(
            'id="', '"', page)))

        # The even values are the teams nickname
        info['Team A'], info['Team B'] = clubs_name[1], clubs_name[3]

        info['ID Team A'], info['ID Team B'] = clubs_id[0], clubs_id[1]
        transfers.append(info)

    return transfers
