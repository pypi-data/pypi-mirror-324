# __init__.py

from .autoupdater import main as auto_update
from .logging_config import setup_logging

# Ensure logging is only initialized once
logger = None

# Package version
__version__ = "0.1.4"

# Flag to ensure that update check happens only once
update_checked = False

# Trigger auto-update when the package is imported, but avoid logging duplication
if not update_checked:
    try:
        if logger is None:  # Only set up logging if not already initialized
            logger = setup_logging()

        logger.info("Checking for updates...")
        auto_update("wangfusamplepackage")  # Call the auto-updater when the package is imported
        update_checked = True  # Set the flag to True after the first check
    except Exception as e:
        if logger is None:  # Initialize logging if an error occurs
            logger = setup_logging()
        logger.error(f"Error during package update check: {e}")
