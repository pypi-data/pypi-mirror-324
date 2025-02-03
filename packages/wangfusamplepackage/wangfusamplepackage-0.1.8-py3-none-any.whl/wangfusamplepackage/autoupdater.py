import subprocess
import sys
import pkg_resources
import requests
import platform
import json

from .logging_config import setup_logging

# Set up logging once when the package is initialized
logger = setup_logging()

def get_python_command():
    """Determine whether to use 'python' or 'python3'."""
    return "python3" if platform.system() != "Windows" else "python"

def get_latest_version(package_name):
    """Fetch the latest version of a package from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        # logger.info(f"Fetching latest version for {package_name} from PyPI...")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data['info']['version']
    except requests.RequestException as e:
        logger.error(f"Network error while fetching {package_name} version: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode the response from PyPI: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while getting latest version: {e}")
    return None

def is_package_installed(package_name):
    """Check if a package is installed."""
    try:
        installed_version = pkg_resources.get_distribution(package_name).version
        # logger.info(f"{package_name} is installed (Version: {installed_version})")
        return installed_version
    except pkg_resources.DistributionNotFound:
        logger.warning(f"{package_name} is not installed.")
        return None
    except Exception as e:
        logger.error(f"Error checking if {package_name} is installed: {e}")
    return None

def install_package(package_name):
    """Install the package via pip."""
    python_cmd = get_python_command()
    try:
        logger.info(f"Installing {package_name}...")
        subprocess.check_call([python_cmd, "-m", "pip", "install", "--upgrade", package_name])
        logger.info(f"{package_name} installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install {package_name}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during installation of {package_name}: {e}")

def update_package(package_name):
    """Update the package to the latest version."""
    python_cmd = get_python_command()
    try:
        logger.info(f"Updating {package_name}...")
        subprocess.check_call([python_cmd, "-m", "pip", "install", "--upgrade", package_name])
        logger.info(f"{package_name} updated successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to update {package_name}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during update of {package_name}: {e}")

def main(package_name):
    """Main function to check for updates and install them if necessary."""
    installed_version = is_package_installed(package_name)
    latest_version = get_latest_version(package_name)

    if latest_version and installed_version:
        if latest_version != installed_version:
            logger.info(f"New version available: {latest_version}. Installed version: {installed_version}.")
            user_input = input(f"{package_name} is out of date. Do you want to update it to {latest_version}? (y/n): ").strip().lower()
            if user_input == 'y':
                update_package(package_name)
            else:
                logger.info(f"{package_name} will not be updated. Exiting...")
                sys.exit(1)
        # else:
        #     logger.info(f"{package_name} is up to date (Version: {installed_version}).")
    elif installed_version is None:
        logger.info(f"{package_name} is not installed. Proceeding with installation.")
        install_package(package_name)
