import logging
import sys

import requests

from page_loader.cli import get_args
from page_loader.logger import configure_logger
from page_loader.page_loader import download



# def download():
#     args = get_args()
#     url, output_dir, verbosity_level = args.URL, args.output, args.verbose
#     configure_logger(verbosity_level)
#     logger = logging.getLogger('page_loader')
#     logger.debug(f'{url}, {output_dir}, {verbosity_level}')
#     try:
#         prepare_directory(output_dir, url)
#     except OSError as e:
#         logger.critical(e)
#         sys.exit(1)
#     try:
#         html_path = save_html(output_dir, url, verbosity_level)
#     except requests.exceptions.HTTPError as e:
#         logger.critical(e)
#         sys.exit(1)
#     print(html_path)


if __name__ == '__main__':
    args = get_args()
    url, output_dir, verbosity_level = args.URL, args.output, args.verbose
    configure_logger(verbosity_level)
    path_to_html = download(url, output_dir)
    print(path_to_html)
