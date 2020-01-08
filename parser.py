""" Parser Module for Transfermarkt Crawler."""
import re
from headers import TRANSFERS, PLAYERS, TEAMS, MANAGERS, MANAGER_HISTORY


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


def parse_in_tags(page, join=True):
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
            pages[index] = remove_tokens(pag, ['\t', '\n', '<', '>', '',
                                               '</th>', '<td>', '<br>'])

        if join:
            return ''.join(pages)

        return list(filter(lambda x: x not in ['', '&nbsp;'], pages))

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

        if not pages:
            return None
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


def league_result_assemble(link, season):
    """ Mount a link of a league results. """
    return link + season


def player_link_assemble(player_name, player_id):
    """ Mount a link of a player getting his history."""

    link = "transfermarkt.com/" + player_name.replace(' ', '-')

    return link + "/profil/spieler/" + str(player_id)


def titles_link_assemble(team_name, team_id):
    """ Mount a link to get all titles of a club."""

    link = "transfermarkt.com/" + team_name.replace(' ', '-')

    return link + '/erfolge/verein/' + str(team_id)


def manager_link_assemble(manager_name, manager_id):
    """Mount a link with manager infos."""

    link = "www.transfermarkt.com/" + manager_name.replace(' ', '-')

    return link + '/profil/trainer/' + str(manager_id)


def manager_detailed_link(manager_name, manager_id):
    """ Mount detailed history link. """

    link = "www.transfermarkt.com/" + manager_name.replace(' ', '-')

    return link + '/profil/trainer/' + str(manager_id) + 'plus/1'


def file_write(team_info, players_info, managers_info):
    """ Write a file with team info.

        players_info = list = each element is a
        dict with players info
        season = int = collect season

        Responsible for create/alterate a file.

        Two files will be change along time:
            transfer.txt - Will store all gathered transfers.
            player.txt - Will store all gathered players
            teams.txt - Will store all gathered teams.
            managers.txt
    """

    with open('Output/teams.txt', 'r+') as file:
        save_file(file, TEAMS, team_info)

    with open('Output/players_id.txt', 'r+') as file:
        players_info = verify_id(file, players_info)

    with open('Output/players.txt', 'r+') as file:
        for player in players_info:
            print(player)
            save_file(file, PLAYERS, player)

    with open('Output/transfers.txt', 'r+') as file:
        transfers = list(map(lambda x: x['Transfers'],
                             players_info))
        for transfer in transfers:
            save_file(file, TRANSFERS, transfer)

    with open('Output/managers_id.txt', 'r+') as file:
        managers_info = verify_id(file, managers_info)

    with open('Output/managers.txt', 'r+') as file:
        for manager in managers_info:
            save_file(file, MANAGERS, manager)

    with open('Output/managers_history.txt', 'r+') as file:
        historic = list(map(lambda x: x['History'],
                            managers_info))
        for history in historic:
            save_file(file, MANAGER_HISTORY, history)


def verify_id(file, data):
    """ Verify repeated ids and remove them from the list."""
    ids = file.readlines()

    data = list(filter(lambda x: str(x['Id']) not in ids,
                       data))

    info = [str(player['Id']) for player in data]

    file.write('\n'.join(info))

    return data


def save_file(file, header, data):
    """ Generic function to save in a database."""
    if data is not None:
        values = list(map(lambda value: str(value), data))
        file.write('\t'.join(values) + '\n')


def write_header(file, header):
    """ Generic function to save the header in a dataset."""
    for index, feature in enumerate(header):
        if index != len(header) - 1:
            file.write(feature + "\t")
        else:
            file.write(feature + "\n")


def parse_season(season):
    """ Get the season in a soccer format: 2000 --> 00/01."""

    season = ''.join(list(str(season))[2:])  # get the two last values
    if season == '99':
        return '99/00'

    if int(season) == 9:
        return "09/10"

    return season + '/' + str(int(season) + 1)
