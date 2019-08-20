""" Responsible to collect the managers info from Transfermarkt"""
import parser
import crawler


def get_manager_info(manager_name, manager_id):
    """ Get managers info. """
    link = parser.manager_link_assemble(manager_name, manager_id)
    manager_page = crawler.get_page(link)
    manager_info = {}
    manager_info['Name'] = manager_name
    manager_info['Id'] = manager_id

    token = "Date of Birth:"
    manager_info['Birth Date'] = parser.retrieve_in_tags(token, "</td>",
                                                         manager_page)

    token = "Place of Birth:"
    manager_info['Birth Place'] = parser.retrieve_in_tags(token, "</td>",
                                                          manager_page)

    token = 'itemprop="nationality">'
    manager_info['Nationality'] = parser.retrieve_in_tags(token, "</span>",
                                                          manager_page)

    token = "Avg. term as manager"
    manager_info['Avg. term'] = parser.retrieve_in_tags(token, "<br/>",
                                                        manager_page)

    token = "Coaching Licence:"
    manager_info['Coaching License'] = parser.retrieve_in_tags(token, "</td>",
                                                               manager_page)

    token = "Preferred Formation"
    manager_info[token] = parser.retrieve_in_tags(token + ':', "</td>",
                                                  manager_page)

    # TODO: Titles, History, I will have to make two more files, managers_id and manager history
