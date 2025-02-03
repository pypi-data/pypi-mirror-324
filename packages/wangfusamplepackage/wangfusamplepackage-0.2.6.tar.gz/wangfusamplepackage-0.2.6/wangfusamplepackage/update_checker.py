# wangfusamplepackage/update_checker.py

import json
import os
from datetime import datetime, timedelta

# Absolute path to the module directory (where your Python package is stored)
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))  # This will give the folder where this script resides
LAST_UPDATED_FILE = os.path.join(MODULE_DIR, 'last_updated.json')  # Path for the JSON file

def load_last_update_time():
    """
    Load the last update time from the JSON file.
    Returns:
        datetime: Last update timestamp, or None if no update exists.
    """
    if os.path.exists(LAST_UPDATE_FILE):
        try:
            with open(LAST_UPDATE_FILE, 'r') as file:
                data = json.load(file)
                last_update_time = datetime.fromisoformat(data['last_updated'])
                print("Loaded last update time from file.")
                return last_update_time
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading last update time from file: {e}")
            return None
    else:
        print("No last update file found.")
        return None

def save_last_update_time():
    """
    Save the current timestamp as the last update time in the JSON file.
    """
    print("sdf")
    now = datetime.now().isoformat()
    try:
        with open(LAST_UPDATE_FILE, 'w') as file:
            json.dump({'last_updated': now}, file)
        print("Last update time saved to file.")
    except Exception as e:
        print(f"Error saving last update time: {e}")

def should_check_for_updates(interval_days=1):
    """
    Check if the package should check for updates based on the given interval in days.
    :param interval_days: The number of days after which the update check should occur.
    :return: True if an update is needed, False otherwise.
    """
    last_update_time = load_last_update_time()
    if last_update_time is None:
        # If no last update, proceed with the update
        print("No last update timestamp found. Proceeding with update check.")
        return True

    time_delta = datetime.now() - last_update_time
    if time_delta > timedelta(days=interval_days):
        print(f"More than {interval_days} days have passed since the last update.")
        return True
    else:
        print(f"Last update was {time_delta.days} days ago, within the check interval.")
        return False
