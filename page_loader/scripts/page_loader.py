import argparse
import os
import os.path
import requests
import re
import urllib.parse
from logging_page_loader import get_logger
from logging_page_loader import configure_logger_verbosity
from bs4 import BeautifulSoup
import sys
from progress.bar import Bar
import time


def get_html(URL):
    r = requests.get(URL)
    return (r.text, r.status_code)


def gen_name_file(URL):
    parts_file_name = re.findall(r'[^\W]+', URL)
    file_name = '-'.join(parts_file_name)
    return file_name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('URL',
                        type=str,
                        help='URL')
    parser.add_argument('--output',
                        type=str,
                        help='path to download page',
                        default=os.getcwd())
    parser.add_argument('--verbose',
                        '-v',
                        action='count',
                        default=0)
    args = parser.parse_args()
    URL = args.URL
    PATH_DIR = args.output
    LEVEL_LOGGING = args.verbose
    logger = configure_logger_verbosity(get_logger(), LEVEL_LOGGING)

    PATH_FILE_HTML = os.path.join(PATH_DIR, gen_name_file(os.path.split(URL)[1]) + '.html')
    PATH_DIR_FILES = os.path.join(PATH_DIR, gen_name_file(os.path.split(URL)[1]) + '_files')

    if os.path.exists(PATH_DIR):
        logger.info(f'Directory "{PATH_DIR}" - exist')
    else:
        logger.critical(f'Directory {PATH_DIR} not exist!')
        sys.exit(1)
    if  not os.access(PATH_DIR, os.W_OK):
        logger.critical(f'Directory {PATH_DIR} not access to Write!')
        sys.exit(1)
    try:
        os.mkdir(PATH_DIR_FILES)
        logger.info(f'"{PATH_DIR_FILES}" - created')
    except FileExistsError:
        logger.info(f'Directory "{PATH_DIR_FILES}" was created earlier')


    try:
        HTML, HTTP_CODE = get_html(URL)
    except (ValueError, requests.exceptions.ConnectionError):
        logger.debug(f'URL - {URL}')
        logger.critical(f'Invalid URL')
        sys.exit(1)
    else:
        logger.info('HTML download')

    if HTTP_CODE == 200:
        logger.info('Code 200. OK')
    elif HTTP_CODE == 404:
        logger.critical('404 Not Found')
        sys.exit(1)
    elif HTTP_CODE == 503:
        logger.critical('503 Server Unavailable')
        sys.exit(1)

    soup = BeautifulSoup(HTML, "lxml")
    logger.debug(f'URL: {URL}')
    logger.debug(f'Path to DIR: {PATH_DIR}')
    logger.debug(f'Path to the directory with files: {PATH_DIR_FILES}')


    logger.info('Write src to file')

    bar = Bar('Processing', max=20)
    for i in range(20):
        time.sleep(3)
        bar.next()
    bar.finish()

    for tag in soup.find_all(['img', 'link', 'script'], src=True):
        split_url = urllib.parse.urlsplit(tag['src'])
        if split_url.scheme or not tag['src']:
            continue
        file_name, file_extension = os.path.splitext(split_url.netloc + split_url.path)
        data_local_resource = requests.get(urllib.parse.urljoin(URL, tag['src'])).text
        path_local_file = os.path.join(PATH_DIR_FILES, gen_name_file(file_name) + file_extension)
        with open(path_local_file, 'w') as file:

            logger.debug(f'Path to file: {path_local_file}')
            file.write(data_local_resource)
        tag['src'] = os.path.join(gen_name_file(os.path.split(URL)[1]) + '_files',
                                  gen_name_file(file_name) + file_extension)
    with open(PATH_FILE_HTML, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    logger.info('Done')


if __name__ == '__main__':
    main()
