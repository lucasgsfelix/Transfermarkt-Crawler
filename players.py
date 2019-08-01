""" Crawler the players from Transfermarkt. """
import parser


def get_player(player_name, player_id):
    """ Get the information about a player. """

    link = parser.player_link_assemble(player_name, player_id)
    player_page = parser.get_page(link)
    player_keys = parser.file_read("Input/players_keys.txt").split("\n")
    player_info = {key: None for key in player_keys}

    player_info['Name'] = player_name
    player_info['Full Name'] = parser.retrieve_in_tags("Full Name:</th>",
                                                       "</td>", player_page)
    player_info['Birth Date'] = parser.retrieve_in_tags("Date of Birth:",
                                                        "</a>", player_page)
