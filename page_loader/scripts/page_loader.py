import argparse
import os
import os.path
import requests
import re
import urllib.parse
from page_loader.logging_page_loader import get_logger
from page_loader.logging_page_loader import configure_logger_verbosity
from bs4 import BeautifulSoup


def get_html(URL):
    r = requests.get(URL)
    return r.text


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
    HTML = get_html(URL)
    PATH_FILE_HTML = os.path.join(PATH_DIR, gen_name_file(os.path.split(URL)[1]) + '.html')
    PATH_DIR_FILES = os.path.join(PATH_DIR, gen_name_file(os.path.split(URL)[1]) + '_files')

    logger = get_logger()
    configure_logger_verbosity(logger, LEVEL_LOGGING)
    soup = BeautifulSoup(HTML, "lxml")
    logger.debug(f'URL: {URL}')
    logger.debug(f'Path to DIR: {PATH_DIR}')
    logger.debug(f'Path to the directory with files: {PATH_DIR_FILES}')
    try:
        os.makedirs(PATH_DIR_FILES)
        logger.info('Dir created: Done')
    except FileExistsError:
        logger.info('URL was downloaded earlier')

    logger.info('Write src to file')
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
