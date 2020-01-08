""" Crawler for Transfermarkt Website"""
from selenium import webdriver


class TimeOutException(Exception):
    """ Time out Exception Class."""


def get_page(link, error=False):
    """ Load and return a web page. """
    if "https://" not in link:
        link = "https://" + link

    html_code = "return document.getElementsByTagName('html')[0].innerHTML"

    if error:
        driver = webdriver.Chrome(chrome_options=_change_proxy())
    else:
        driver = webdriver.Chrome()

    try:
        driver.get(link)
        html = driver.execute_script(html_code)
    except:
        driver.refresh()
        driver.get(link)
        html = driver.execute_script(html_code)

    driver.close()

    return html


def _change_proxy():
    """ Change proxy and port of the browser. """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.accept_untrusted_certs = True
    chrome_options.assume_untrusted_cert_issuer = True
    chrome_options.add_argument('--proxy-server=46.102.106.37:13228')

    return chrome_options
