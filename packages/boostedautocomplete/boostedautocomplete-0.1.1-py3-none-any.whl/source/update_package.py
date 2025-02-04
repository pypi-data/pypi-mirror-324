import subprocess
import sys
import pkg_resources
import requests
import platform
import json
from .update_checker import save_last_update_time

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
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def is_package_installed(package_name):
    # Check if a package is installed
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        print(f"{package_name} is not installed.")
    except Exception as e:
        print(f"Error checking if {package_name} is installed: {e}")
    return None
    
def get_installed_version(package_name):
    # Get the installed version of a package
    try:
        return pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        return None

def install_or_update_package(package_name, action="install"):
    
    # install or update a package using pip
    python_cmd = get_python_command()
    action_str = "Installing" if action == "install" else "Updating"

    try:
        print(f"{action_str} {package_name}...")
        subprocess.check_call([python_cmd, "-m", "pip", "install", "--upgrade", package_name])
        print(f"{package_name} {action.lower()}ed successfully")
        save_last_update_time()

    except subprocess.CalledProcessError as e:
        print(f"Failed to {action.lower()} {package_name}: {e}")
    except Exception as e:
        print(f"Unexpected error during {action.lower()} of {package_name}: {e}")
    


def main(package_name):
    # Check installation, and update if necessary

    installed_version = is_package_installed(package_name)
    latest_version = get_latest_version(package_name)

    if latest_version and installed_version:
        if latest_version != installed_version:
            print(f"New version available: {latest_version}. Installed version: {installed_version}")
            user_input = input(f"{package_name} is out of date. update to {latest_version}? (y/n):").strip().lower()
            if user_input == 'y':
                install_or_update_package(package_name, action="update")
            else:
                print(f"{package_name} update skipped.")
        else:
            print(f"{package_name} is up to date")
    elif not installed_version:
        print(f"{package_name} is not installed. installing...")
        install_or_update_package(package_name, action="install")