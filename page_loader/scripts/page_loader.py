import os.path
import urllib.parse
import sys
from progress.bar import Bar
from page_loader import cli
from page_loader.logging_page_loader import get_logger, \
    configure_logger_verbosity
from page_loader.dir_and_file import create_dir, is_valid_dir, gen_name, \
    write_to_file
from page_loader.work_to_http import get_data, get_html, is_valid_status
from page_loader.work_to_html import get_local_links, change_link


def main():
    args = cli.get_args()
    # args = get_args()
    URL, PATH_DIR, LEVEL_LOGGING = args['url'], args['output'], args['verbose']
    NAME_FILE_HTML = gen_name(URL) + '.html'
    NAME_DIR_FILES = gen_name(URL) + '_files'
    logger = configure_logger_verbosity(get_logger(), LEVEL_LOGGING)
    logger.debug(f'URL: {URL}')
    logger.debug(f'Path to DIR: {PATH_DIR}')
    logger.debug(f'Name Dir_files: {NAME_DIR_FILES}')
    if not is_valid_dir(PATH_DIR):
        sys.exit(1)
    create_dir(os.path.join(PATH_DIR, NAME_DIR_FILES))
    logger.info(f'{URL}: Download...')
    html, http_response = get_html(URL)
    if not is_valid_status(http_response):
        sys.exit(1)
    local_links = get_local_links(html)
    if LEVEL_LOGGING == 0:
        bar = Bar('Processing', max=len(local_links))
    logger.info('Processing: download local links')
    for link in local_links:
        if LEVEL_LOGGING == 0:
            bar.suffix = '%(index)d/%(max)d ' + link
            bar.next()
        split_url = urllib.parse.urlsplit(link).netloc + urllib.parse.urlsplit(
            link).path
        url = urllib.parse.urljoin(URL, split_url)
        data = get_data(url)
        name_file = gen_name(link, ext=True)
        write_to_file(path=os.path.join(PATH_DIR, NAME_DIR_FILES, name_file),
                      data=data)
        logger.info(f'File: {link} download to: {NAME_DIR_FILES + name_file}')
        html = change_link(html=html, old_link=link,
                           new_link=os.path.join(NAME_DIR_FILES, name_file))
    write_to_file(path=os.path.join(PATH_DIR, NAME_FILE_HTML), data=html)
    if LEVEL_LOGGING == 0:
        bar.finish()
        print('All Done')


if __name__ == '__main__':
    main()
