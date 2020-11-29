import logging
import os.path
from typing import Any

import requests
import sys

from page_loader.naming import make_name_for_dir_files
from page_loader.network import download_and_save_local_html, \
    download_from_urls
from page_loader.storage import prepare_directory


def download(url: str, output_dir: Any, verbosity_level=0) -> str:
    """
    Скачивает html и ресурсы на которые есть локальные ссылки.
    Меняет html что локальные ссылки ведут на ресурсы которые скачаны
    """
    logger = logging.getLogger('page_loader')
    logger.debug(f'{url}, {output_dir}, {verbosity_level}')
    path = output_dir if isinstance(output_dir, str) else output_dir()
    download_dir = os.path.join(path, make_name_for_dir_files(url))
    try:
        prepare_directory(path, url)
    except OSError as e:
        logger.critical(e)
        sys.exit(1)
    try:
        html_path, download_urls = download_and_save_local_html(path, url)
    except requests.exceptions.HTTPError as e:
        logger.critical(e)
        sys.exit(1)
    download_from_urls(urls=download_urls, download_dir=download_dir,
                       verbosity=verbosity_level)
    return html_path
