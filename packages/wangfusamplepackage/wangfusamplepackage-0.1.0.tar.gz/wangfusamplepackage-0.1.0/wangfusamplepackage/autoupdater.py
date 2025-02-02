import subprocess
import sys
import pkg_resources
import requests
import platform
import json

def get_python_command():
    # Determine whether to use 'python' or 'python3'
    return "python3" if platform.system() != "Windows" else "python"

def get_latest_version(package_name):
    # Fetch the latest version of a package from PyPI
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data['info']['version']
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Erro fetching the latest version: {e}")
        return None

def is_package_installed(package_name):
    # Check if a package is installed
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None
    
def get_installed_version(package_name):
    # Get the installed version of a package
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None

def install_package(package_name):
    # Install the package via pip
    python_cmd = get_python_command()
    try:
        subprocess.check_call([python_cmd, "-m", "pip", "install", "--upgrade", package_name])
        print(f"{package_name} installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}")

def update_package(package_name):
    # Update the package to the latest version
    python_cmd = get_python_command()
    try:
        subprocess.check_call([python_cmd, "-m", "pip", "install", "--upgrade", package_name])
        print(f"{package_name} updated successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update {package_name}: {e}")
    


def main(package_name):

    print(f"Checking for updates for {package_name}...")
    
    # Check installation, and update if necessary

    if not is_package_installed(package_name):
        user_input = input(f"{package_name} is not installed. do you want to install it? (y/n):").strip().lower()
        if user_input == 'y':
            install_package(package_name)
        else:
            print(f"{package_name} will not be installed. Exiting...")
            sys.exit(1)
    installed_version = get_installed_version(package_name)
    latest_version = get_latest_version(package_name)

    if latest_version and installed_version != latest_version:
        print(f"Updating {package_name} from {installed_version} to {latest_version}...")
        update_package(package_name)
    else:
        print(f"{package_name} is up to date (Version: {installed_version})")

if __name__ == "__main__":
    print("Starting the autoupdater script...")
    package_name = "wangfusamplepackage"
    main(package_name)
