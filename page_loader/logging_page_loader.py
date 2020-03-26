import logging


def get_logger():
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(format)
    logger.addHandler(handler)
    return logger


def configure_logger_verbosity(logger, verbosity):
    if verbosity == 3:
        logger.setLevel(level=logging.DEBUG)
    elif verbosity == 2:
        logger.setLevel(level=logging.INFO)
    elif verbosity == 1:
        logger.setLevel(level=logging.WARNING)
    else:
        logger.disabled = True
