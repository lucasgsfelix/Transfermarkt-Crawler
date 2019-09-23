"""Responsible to call the results methods"""
import parser
import leagues
from headers import LEAGUE_CLASS


def write_header(header_call):
    '''Write header in the output file'''
    if header_call:
        parser.write_header(OUTPUT_FILE, LEAGUE_CLASS)
        header_call = False
    return header_call


if __name__ == '__main__':

    OUTPUT_FILE = open("Output/league_results.txt", 'a')
    with open("Input/leagues_results.txt", 'r') as LEAGUES_LINKS:
        LEAGUES_LINKS = LEAGUES_LINKS.open().split('\n')
        START = 2005
        END = 2020
        HEADER_CALL = True
        for league in LEAGUES_LINKS:
            for season in range(START, END):
                results = leagues.get_results(league, str(season))
                HEADER_CALL = write_header(HEADER_CALL)
                for result in results:
                    parser.save_file(OUTPUT_FILE, LEAGUE_CLASS, result)
                OUTPUT_FILE.close()
