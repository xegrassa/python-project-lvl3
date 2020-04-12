import requests
import logging

logger = logging.getLogger('page_loader')


def get_data(URL):
    return requests.get(URL).text


def get_html(URL):
    r = requests.get(URL)
    return (r.text, r.status_code)


def is_valid_status(HTTP_CODE):
    if HTTP_CODE == 200:
        logger.info('Code 200. OK')
        return True
    elif HTTP_CODE == 404:
        logger.critical('404 Not Found')
    elif HTTP_CODE == 503:
        logger.critical('503 Server Unavailable')
    return False
