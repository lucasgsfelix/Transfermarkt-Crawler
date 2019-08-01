""" Parser Module for Transfermarkt Crawler."""
import os
import re
import time


def file_read(file):
    """ Read files function. """

    with open(file) as file_data:
        return file_data.read()


def get_page(link):
    """ Download and return a web page. """

    link = link.split('https://')[1] # removing https token

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
    positions = {start_pos[index]: e for index, e in enumerate(end_pos)}

    return list(map(lambda x: page[x:positions[x]], positions))

def remove_token(values, tokens):
    """ Remove a list of tokens from list. """
    return list(filter(lambda x: x not in tokens, values))
