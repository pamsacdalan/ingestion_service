import json
import os
from datetime import datetime

STATE_FILE = "state.json"


def get_last_timestamp():

    if not os.path.exists(STATE_FILE):
        return None
    
    with open(STATE_FILE) as f:
        data = json.load(f)
    
    return data.get("last_timestamp")


def save_last_timestamp(timestamp):

    with open(STATE_FILE, "w") as f:
        json.dump({"last_timestamp": timestamp}, f)
