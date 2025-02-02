# wangfusamplepackage/logging_config.py

import logging
import logging.handlers

def setup_logging(log_file='wangfusamplepackage.log', log_level=logging.DEBUG):
    """
    Setup logging configuration for the package.

    :param log_file: The log file where logs should be written.
    :param log_level: The logging level to use (e.g., DEBUG, INFO, ERROR).
    """
    logger = logging.getLogger('wangfusamplepackage')
    logger.setLevel(log_level)

    # Log formatter
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Create a file handler to log to a file
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10**6, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Create a console handler to log to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Less verbose on console
    console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
