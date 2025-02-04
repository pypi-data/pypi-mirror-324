# __init__.py

__version__ = "0.1.2"

from .update_checker import should_check_for_updates

def perform_update_check(interval_days=1):

    try:
        print("Checking if update is needed...")

        if should_check_for_updates(interval_days):
            print("Update is needed. Starting the update process")

            from .update_package import main as update_package

            update_package("boostedautocomplete")

        else:
            print("No update is needed as this time.")
    except Exception as e:
        print(f"Error updating check: {e}")

perform_update_check(1)