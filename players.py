""" Crawler the players from Transfermarkt. """
import parser


def get_player(player_name, player_id):
    """ Get the information about a player. """

    link = parser.player_link_assemble(player_name, player_id)
    player_page = parser.get_page(link)
    player_info = {}

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
