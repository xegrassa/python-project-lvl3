import logging

import requests
import sys
import os.path

from page_loader.network import download_and_save_local_html, get_data_from_urls, make_name_for_dir_files
from page_loader.storage import prepare_directory


def download(url: str, output_dir: str, verbosity_level=1):
    logger = logging.getLogger('page_loader')
    logger.debug(f'{url}, {output_dir}, {verbosity_level}')
    try:
        prepare_directory(output_dir, url)
    except OSError as e:
        logger.critical(e)
        sys.exit(1)
    try:
        html_path, download_urls = download_and_save_local_html(output_dir, url)
    except requests.exceptions.HTTPError as e:
        logger.critical(e)
        sys.exit(1)

    path = output_dir if isinstance(output_dir, str) else output_dir()
    download_dir = os.path.join(path, make_name_for_dir_files(url))
    get_data_from_urls(urls=download_urls, download_dir=download_dir, verbosity=verbosity_level)

    return html_path
