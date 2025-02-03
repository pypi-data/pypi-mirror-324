# __init__.py

from .autoupdater import main as auto_update
from .logging_config import setup_logging

# Set up logging once when the package is initialized
logger = setup_logging()

# Package version
__version__ = "0.2.1"

# Flag to ensure that update check happens only once
update_checked = False

# Trigger auto-update when the package is imported
if not update_checked:
    try:
        logger.info("Checking for updates...")
        auto_update("wangfusamplepackage")  # Call the auto-updater when the package is imported
        update_checked = True  # Set the flag to True after the first check
    except Exception as e:
        logger.error(f"Error during package update check: {e}")
