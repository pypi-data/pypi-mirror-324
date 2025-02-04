import json
import os
from datetime import datetime, timedelta

# absolute path to the module directory
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
LAST_UPDATE_FILE = os.path.join(MODULE_DIR, 'last_updated_boostedautocomplete.json')

def load_last_update_time():

    if os.path.exists(LAST_UPDATE_FILE):
        try:
            with open(LAST_UPDATE_FILE, 'r') as file:
                data = json.load(file)
                last_update_time = datetime.fromisoformat(data['last_updated'])
                print("Loaded last update time from file")
                return last_update_time
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading last update time from file: {e}")
            return None
    else:
        print("No last update file found.")
        save_last_update_time()
        return None

def save_last_update_time():

    now = datetime.now().isoformat()
    try:
        with open(LAST_UPDATE_FILE, 'w') as file:
            json.dump({'last_updated': now}, file)
        print("Last update time saved to file.")
    except Exception as e:
        print(f"Error saving last update time: {e}")

def should_check_for_updates(interval_days):

    last_update_time = load_last_update_time()
    if last_update_time is None:
        print("No last update time found.")
        return True
    time_delta = datetime.now()- last_update_time
    if time_delta > timedelta(days=interval_days):
        print(f"More than {interval_days} have passed")
    else:
        print(f"Last update was {time_delta.days} days ago.")
        return False