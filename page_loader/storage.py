import logging
import os

from page_loader.naming import make_name_for_dir_files


def check_dir(path):
    """
    Проверка что нужная директория существует и есть права на запись
    """
    if not os.path.exists(path):
        raise OSError(f'Directory {path} not exist!')
    if not os.access(path, os.W_OK):
        raise OSError(f'Directory {path} not access to Write!')


def create_dir_files(path):
    """
    Создание директории под скачанные файлы, проверка что директория пустая
    """
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
    check_dir(path)
    logger.info(f'Directory "{path}" - exist')
    create_dir_files(os.path.join(path, make_name_for_dir_files(url)))
