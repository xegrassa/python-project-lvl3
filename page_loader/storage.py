import logging
import os
import re
import urllib.parse


def make_name_from_url(URL: str) -> str:
    parse_url = urllib.parse.urlsplit(URL)
    url_without_schema = parse_url.netloc + parse_url.path
    if not parse_url.path:
        return replace_symbols(url_without_schema) + '.html'
    root, ext = os.path.splitext(url_without_schema)
    file_name = replace_symbols(root)
    if not ext:
        ext = '.html'
    return file_name + ext


def replace_symbols(string: str) -> str:
    parts_file_name = re.findall(r'[^\W]+', string)
    file_name = '-'.join(parts_file_name)
    return file_name


def convert_url_to_name(URL: str, ext: bool = False) -> str:
    parse_url = urllib.parse.urlsplit(URL)
    url_not_schema = parse_url.netloc + parse_url.path
    if ext:
        url_not_schema, file_ext = os.path.splitext(url_not_schema)
    parts_file_name = re.findall(r'[^\W]+', url_not_schema)
    file_name = '-'.join(parts_file_name)
    if ext:
        return file_name + file_ext
    return file_name


def check_dir(path):
    if not os.path.exists(path):
        raise OSError(f'Directory {path} not exist!')
    if not os.access(path, os.W_OK):
        raise OSError(f'Directory {path} not access to Write!')


def create_dir(path):
    logger = logging.getLogger('page_loader')
    if os.path.exists(path):
        logger.warning(f'DIR: "{path}" was created earlier')
    else:
        os.mkdir(path)
        logger.info(f'DIR: "{path}" - created')
    if os.listdir(path):
        raise OSError(f'DIR: "{path}" not empty!!!')


def write_to_file(path, data):
    if isinstance(data, bytes):
        with open(path, 'wb') as file:
            file.write(data)
    else:
        with open(path, 'w') as file:
            file.write(data)


def prepare_directory(path_dir, url):
    logger = logging.getLogger('page_loader')
    path = path_dir if isinstance(path_dir, str) else path_dir()
    dir_name = convert_url_to_name(url) + '_files'
    check_dir(path)
    logger.info(f'Directory "{path}" - exist')
    create_dir(os.path.join(path, dir_name))
