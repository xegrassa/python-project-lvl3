import os.path
import urllib.parse
from bs4 import BeautifulSoup
import sys
import itertools
from progress.bar import Bar

from page_loader.logging_page_loader import get_logger
from page_loader.logging_page_loader import configure_logger_verbosity
from page_loader import cli
from page_loader.dir_and_file import create_dir, is_valid_dir, gen_name_file, write_to_file
from page_loader.work_to_http import get_data, get_html, is_valid_status
from page_loader.work_to_html import get_local_links, change_link


def is_empty_or_scheme_tag(tag):
    split_url = urllib.parse.urlsplit(tag['src'])
    if split_url.scheme or not tag['src']:
        return True
    return False


def main():
    args = cli.get_args()
    URL, PATH_DIR, LEVEL_LOGGING = args['url'], args['output'], args['verbose']
    PATH_FILE_HTML = os.path.join(PATH_DIR, gen_name_file(os.path.split(URL)[1]) + '.html')
    PATH_DIR_FILES = os.path.join(PATH_DIR, gen_name_file(os.path.split(URL)[1]) + '_files')
    logger = configure_logger_verbosity(get_logger(), LEVEL_LOGGING)
    logger.debug(f'URL: {URL}')
    logger.debug(f'Path to DIR: {PATH_DIR}')
    logger.debug(f'Path to DIR_files: {PATH_DIR_FILES}')
    if not is_valid_dir(PATH_DIR):
        sys.exit(1)
    create_dir(PATH_DIR_FILES)
    html, http_response = get_html(URL)
    if not is_valid_status(http_response):
        sys.exit(1)

    local_links = get_local_links(html)
    for link in local_links:
        name_file = PATH_DIR_FILES + gen_name_file(link)
        data = get_data(urllib.parse.urljoin(URL + link))
        write_to_file(path=name_file, data=data)
        # html = change_link(html=html, old_link=link, new_link=name_file)
    write_to_file(path=PATH_FILE_HTML, data=html)

    # soup = BeautifulSoup(HTML, "lxml")
    # tags = soup.find_all(['img', 'link', 'script'], src=True)
    # tags_include_src = list(itertools.filterfalse(is_empty_or_scheme_tag, tags))
    # logger.info('Write src to file')
    # if LEVEL_LOGGING == 0: bar = Bar('Processing', max=len(tags_include_src))
    # for tag in tags_include_src:
    #     if LEVEL_LOGGING == 0:
    #         bar.suffix = '%(index)d/%(max)d ' + tag['src']
    #         bar.next()
    #     split_url = urllib.parse.urlsplit(tag['src'])
    #     file_name, file_extension = os.path.splitext(split_url.netloc + split_url.path)
    #     url_data = urllib.parse.urljoin(URL, tag['src'])
    #     path_local_file = os.path.join(PATH_DIR_FILES, gen_name_file(file_name) + file_extension)
    #     with open(path_local_file, 'w') as file:
    #         file.write(get_data(url_data))
    #     logger.debug(f"Write Data from {tag['src']} to {path_local_file}")
    #     tag['src'] = os.path.join(gen_name_file(os.path.split(URL)[1]) + '_files',
    #                               gen_name_file(file_name) + file_extension)
    # with open(PATH_FILE_HTML, 'w', encoding='utf-8') as file:
    #     file.write(str(soup))
    # logger.info('Done')
    #
    # if LEVEL_LOGGING == 0:
    #     bar.finish()
    #     print('All Done')


if __name__ == '__main__':
    main()
