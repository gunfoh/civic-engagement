import json
import os

DATA_FILE = "civic_issues.json"

def load_data():
    
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            #handle case where file is empty
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(database):
    
    with open(DATA_FILE, 'w') as f:
        json.dump(database, f, indent=4)
