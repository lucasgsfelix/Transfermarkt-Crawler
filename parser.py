""" Parser Module for Transfermarkt Crawler."""
import re
from headers import TRANSFERS, PLAYERS


def file_read(file_name):
    """ Read files function. """
    try:
        with open(file_name) as file_data:
            return file_data.read()
    except UnicodeDecodeError:
        with open(file_name, encoding='latin-1') as file_data:
            return file_data.read()


def cut_page(start_token, end_token, page):
    """ Cut the page.

        Cut the page in the start_token, and then
        the first token that matchs with the position
        bigger than the position of the start token.

        return cut of the page
    """
    start_pos = [(a.end()) for a in list(re.finditer(start_token, page))]

    if start_pos:
        start_pos = start_pos[0]
        end_pos = [(a.start()) for a in list(re.finditer(end_token, page))]
        end_pos = list(filter(lambda x: x > start_pos, end_pos))[0]

        return page[start_pos:end_pos]

    return page


def _match_positions(start_list, end_list):
    """ Match start and end positions. """

    if len(start_list) == 1:
        value = start_list[0]
        return {value: list(filter(lambda x: value < x, end_list))[0]}

    result = {}
    for start in start_list:
        for end in end_list:
            if start < end:
                result[start] = end
                break

    return result


def remove_tokens(page, tokens):
    """ Remove tokens from the page. """
    for token in tokens:
        page = list(filter((token).__ne__, page))

    if '  ' in ''.join(page):
        text_aux = ''
        for pag in ''.join(page).split(' '):
            if pag:
                text_aux += pag + ' '

        return ''.join(text_aux[:-1])

    return ''.join(page)


def parse_in_tags(page):
    """ Parse between > and < tags. """

    if '>' in page:
        pages = []
        start_pos = [(a.end()) for a in list(re.finditer('>', page))]
        for pos in start_pos:
            aux = pos
            while aux <= len(page)-1 and page[aux] != '<':
                aux += 1
            pages.append(page[pos:aux])

        for index, pag in enumerate(pages):
            pages[index] = remove_tokens(pag, ['\t', '\n', '<', '>', ''])

        return ''.join(pages)

    return page


def retrieve_in_tags(start_token, end_token, page, parse=True):
    """ Retrieve between tags.

        Given a start_token and a end_token, will retrieve
        all values between those two tags.

        return parsed values
    """
    start_pos = [(a.end()) for a in list(re.finditer(start_token, page))]

    if not start_pos:
        return None

    end_pos = [(a.start()) for a in list(re.finditer(end_token, page))]

    positions = _match_positions(start_pos, end_pos)

    pages = list(map(lambda x: page[x:positions[x]], positions))

    if parse:
        for index, pag in enumerate(pages):
            pages[index] = parse_in_tags(pag)

        if len(set(pages)) > 1:
            return pages
        return pages[0]

    return pages


def remove_token(values, tokens):
    """ Remove a list of tokens from list. """
    return list(filter(lambda x: x not in tokens, values))


def team_detailed_link_assemble(team_name, team_id, season):
    """ Mount a link of a team getting the with it transfers. """

    link = "transfermarkt.com/" + team_name.replace(' ', '-').lower()

    club = "/transfers/verein/" + str(team_id)

    season = "/saison_id/" + str(season)

    detailed = "/pos//detailpos/0/w_s//plus/1#zugaenge"

    return link + club + season + detailed


def team_link_assemble(team_name, team_id, season):
    """ Mount a not detailed link of a team. """

    link = "transfermarkt.com/" + team_name.replace(' ', '-').lower()

    club = "/transfers/verein/" + str(team_id)

    season = "?saison_id=" + str(season)

    return link + club + season


def player_link_assemble(player_name, player_id):
    """ Mount a link of a player getting his history."""

    link = "transfermarkt.com/" + player_name.replace(' ', '-')

    return link + "/profil/spieler/" + str(player_id)


def titles_link_assemble(team_name, team_id):
    """ Mount a link to get all titles of a club."""

    link = "transfermarkt.com/" + team_name.replace(' ', '-')

    return link + '/erfolge/verein/' + str(team_id)


def manager_link_assemble():
    """Mount a link with manager infos."""


def file_write(team, players_info, season):
    """ Write a file with team info.

        players_info = list = each element is a
        dict with players info
        season = int = collect season

        Responsible for create/alterate a file.

        Two files will be change along time:
            transfer.txt - Will store all gathered transfers.
            player.txt - Will store all gathered players
            teams.txt - Will store all gathered teams.
    """

    with open('Output/teams.txt', 'a') as file:
        pass

    with open('Output/players_id.txt', 'a') as file:

        players_id = file.read().split('\n')

        players_info = list(filter(lambda x: x['Id'] not in players_id,
                                   players_info))

        for player_id in players_info:
            file.write(player_id['Id'] + "\n")

    with open('Output/transfers.txt', 'a') as file:
        for transfer in players_info['Transfers']:
            save_file(file, TRANSFERS, transfer)

    with open('Output/players.txt', 'a') as file:
        for player in players_info:
            save_file(file, PLAYERS, player)

        # TODO: make a function to better print this data set


def save_file(file, header, data):
    """ Generic function to save in a database."""
    for index, key in enumerate(header):
        if index != len(header) - 1:
            file.write(data[key] + "\t")
        else:
            file.write(data[key] + "\n")


def parse_season(season):
    """ Get the season in a soccer format: 2000 --> 00/01."""

    season = ''.join(list(str(season))[2:])  # get the two last values
    if season == '99':
        return '99/00'

    if int(season) == 9:
        return "09/10"

    return season + '/' + str(int(season) + 1)
