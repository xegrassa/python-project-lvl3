import logging


def configure_logger(verbosity=0):
    logger = logging.getLogger('page_loader')
    handler = logging.StreamHandler()
    format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(format)
    logger.addHandler(handler)
    if verbosity == 3:
        logger.setLevel(level=logging.DEBUG)
    elif verbosity == 2:
        logger.setLevel(level=logging.INFO)
    elif verbosity == 1:
        logger.setLevel(level=logging.WARNING)
    else:
        logger.disabled = True
