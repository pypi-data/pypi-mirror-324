import logging

def setup_logging():
    """Configures logging for the application."""
    logging.basicConfig(
        level=logging.INFO,  # Set logging level to INFO
        format="%(asctime)s - %(levelname)s - %(message)s"  # Set log message format
    )
    return logging.getLogger()  # Return the root logger
