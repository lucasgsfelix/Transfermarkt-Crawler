""" Parser Module for Transfermarkt Crawler."""
import os
import re


def file_read(file):
    """ Read files function. """

    with open(file) as file_data:
        return file_data.read()


def get_page(link):
    """ Download and return a web page. """
    if "https://" in link:
        link = link.split('https://')[1]

    os.system('wget -O file.html ' + link + " --quiet")
    file_data = file_read('file.html')
    os.system('rm file.html')

    return file_data


def cut_page(start_token, end_token, page):
    """ Cut the page.

        Cut the page in the start_token, and then
        the first token that matchs with the position
        bigger than the position of the start token.

        return cut of the page
    """
    start_pos = [(a.end()) for a in list(re.finditer(start_token, page))][0]
    end_pos = [(a.start()) for a in list(re.finditer(end_token, page))]

    end_pos = list(filter(lambda x: x > start_pos, end_pos))[0]

    return page[start_pos:end_pos]


def retrieve_in_tags(start_token, end_token, page):
    """ Retrieve between tags.

        Given a start_token and a end_token, will retrieve
        all values between those two tags.

        return parsed values
    """
    start_pos = [(a.end()) for a in list(re.finditer(start_token, page))]
    end_pos = [(a.start()) for a in list(re.finditer(end_token, page))]

    # Gives a dictionary with key start position and value end position
    positions = {s: end_pos[index] for index, s in enumerate(start_pos)}

    return list(map(lambda x: page[x:positions[x]], positions))


def remove_token(values, tokens):
    """ Remove a list of tokens from list. """
    return list(filter(lambda x: x not in tokens, values))


def team_link_assemble(team_name, team_id, season):
    """ Mount a link of a team getting the with it transfers. """

    link = "transfermarkt.com/" + team_name.replace(' ', '-')

    club = "/transfers/verein/" + str(team_id)

    season = "/saison_id/" + str(season)

    detailed = "/pos//detailpos/0/w_s//plus/1#zugaenge"

    return link + club + season + detailed


def player_link_assemble(player_name, player_id):
    """ Mount a link of a player getting his history"""

    link = "transfermarkt.com/" + player_name.replace(' ', '-')

    return link + "/profil/spieler/" + str(player_id)
