import logging
import sys

import requests

# from page_loader.cli import get_args
# from page_loader.Logging import configure_logger
# from page_loader.network import save_html
# from page_loader.storage import prepare_directory


from cli import get_args
from Logging import configure_logger
from network import save_html
from storage import prepare_directory


def main():
    args = get_args()
    url, path_dir, verbosity_level = args.URL, args.output, args.verbose
    configure_logger(verbosity_level)
    logger = logging.getLogger('page_loader')
    logger.debug(f'{url}, {path_dir}, {verbosity_level}')
    try:
        prepare_directory(path_dir, url)
    except OSError as e:
        logger.critical(e)
        sys.exit(1)
    try:
        save_html(path_dir, url, verbosity_level)
    except requests.exceptions.HTTPError as e:
        logger.critical(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
