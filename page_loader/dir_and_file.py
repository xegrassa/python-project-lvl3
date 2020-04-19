import os
import logging
import re
import os.path
import urllib.parse

logger = logging.getLogger('page_loader')


def gen_name(URL, ext=False):
    parse_url = urllib.parse.urlsplit(URL)
    url_not_schema = parse_url.netloc + parse_url.path
    if ext:
        url_not_schema, file_ext = os.path.splitext(url_not_schema)
    parts_file_name = re.findall(r'[^\W]+', url_not_schema)
    file_name = '-'.join(parts_file_name)
    if ext:
        return file_name + file_ext
    return file_name


def is_valid_dir(PATH_DIR):
    if os.path.exists(PATH_DIR):
        logger.info(f'Directory "{PATH_DIR}" - exist')
    else:
        logger.critical(f'Directory {PATH_DIR} not exist!')
        return False
    if not os.access(PATH_DIR, os.W_OK):
        logger.critical(f'Directory {PATH_DIR} not access to Write!')
        return False
    return True


def create_dir(path_dir):
    try:
        os.mkdir(path_dir)
        logger.info(f'DIR: "{path_dir}" - created')
    except FileExistsError:
        logger.warning(f'DIR: "{path_dir}" was created earlier')


def write_to_file(path, data=''):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(data)
