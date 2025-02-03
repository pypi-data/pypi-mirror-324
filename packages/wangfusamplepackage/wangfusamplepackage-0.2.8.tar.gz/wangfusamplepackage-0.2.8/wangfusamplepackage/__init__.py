# __init__.py

# Package version
__version__ = "0.2.8"

from .update_checker import should_check_for_updates

def perform_update_check():
    """
    Check if the package needs an update. If so, trigger the update process.
    """
    try:
        print("Checking if update is needed...")

        if should_check_for_updates(interval_days=1):  # Check if 1 day has passed since the last update
            print("Update is needed. Starting the update process...")

            # Import autoupdater only when needed to prevent slow loading
            from .update_package import main as update_package

            # Perform the update
            update_package("wangfusamplepackage")

        else:
            print("No update is needed at this time.")
    
    except Exception as e:
        print(f"An error occurred during the update check: {e}")

# Perform the update check automatically when the package is imported
perform_update_check()
