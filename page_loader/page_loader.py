import logging

import requests
import sys

from page_loader.network import save_html
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
        html_path = save_html(output_dir, url, verbosity_level)
    except requests.exceptions.HTTPError as e:
        logger.critical(e)
        sys.exit(1)
    return html_path
