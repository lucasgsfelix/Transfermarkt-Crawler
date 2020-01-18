""" Responsible to collect the managers info from Transfermarkt"""
import parser
import crawler


def get_manager_info(manager_name, manager_id):
    """ Get managers info. """
    link = parser.manager_link_assemble(manager_name, manager_id)
    manager_page = crawler.get_page(link)

    manager_info = {}
    manager_info['Name'] = manager_name.replace('-', ' ')
    manager_info['Id'] = manager_id

    token = "Date of Birth:"
    manager_info['Birth Date'] = parser.retrieve_in_tags(token, "</td>",
                                                         manager_page)

    token = 'itemprop="birthPlace">'
    manager_info['Birth Place'] = parser.retrieve_in_tags(token, "</span>",
                                                          manager_page)

    token = 'itemprop="nationality">'
    manager_info['Nationality'] = parser.retrieve_in_tags(token, "</span>",
                                                          manager_page)

    token = "Avg. term as manager:"
    manager_info['Avg. term'] = parser.retrieve_in_tags(token, "</td>",
                                                        manager_page)

    token = "Coaching Licence:"
    manager_info['Coaching License'] = parser.retrieve_in_tags(token, "</td>",
                                                               manager_page)

    token = "Preferred Formation"
    manager_info[token] = parser.retrieve_in_tags(token + ':', "</td>",
                                                  manager_page)

    manager_info['History'] = get_manager_history(manager_name, manager_id)

    return manager_info


def get_manager_history(manager_name, manager_id):
    ''' Get all team that a manager worked. '''
    link = parser.manager_detailed_link(manager_name, manager_id)
    manager_page = crawler.get_page(link)

    begin_token = '<td class="zentriert no-border-rechts">'
    end_token = '</tr>'
    stories = parser.retrieve_in_tags(begin_token, end_token,
                                      manager_page, False)
    if stories is None:
        return None

    history = []
    for story in stories:
        info = {}
        info['Manager Id'] = manager_id
        info['Team'] = parser.retrieve_in_tags('alt="', '"', story, False)[0]
        info['Id'] = set(parser.retrieve_in_tags('id="', '"', story, False))
        tokens_tag = parser.parse_in_tags(story, False)
        info['Appointed'] = tokens_tag[1].replace("&nbsp;", '')
        info['Contract'] = tokens_tag[2].replace("&nbsp;", '')
        info['Position'] = tokens_tag[3]
        info['\\# Matches'] = tokens_tag[4]
        info['Points Per Match'] = tokens_tag[5]
        history.append(info)

    return history
