""" Parser Module for Transfermarkt Crawler."""
import os
import re


def file_read(file_name):
    """ Read files function. """

    with open(file_name) as file_data:
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


def team_link_assemble(team_name, team_id, season):
    """ Mount a link of a team getting the with it transfers. """

    link = "transfermarkt.com/" + team_name.replace(' ', '-').lower()

    club = "/transfers/verein/" + str(team_id)

    season = "/saison_id/" + str(season)

    detailed = "/pos//detailpos/0/w_s//plus/1#zugaenge"

    return link + club + season + detailed


def player_link_assemble(player_name, player_id):
    """ Mount a link of a player getting his history"""

    link = "transfermarkt.com/" + player_name.replace(' ', '-')

    return link + "/profil/spieler/" + str(player_id)


def file_write(file_name, team_info):
    """ Write a file with team info. """

    with open(file_name, 'a') as write_file:
        print(team_info)
        exit()
