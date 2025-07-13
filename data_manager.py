import json
import os

DATA_FILE = "civic_issues.json"

def load_data():
    """
    Loads the issue data from the JSON file.
    If the file doesn't exist or is empty, it returns an empty list.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            # Handle case where file is empty
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_data(database):
    """
    Saves the provided list of issues to the JSON file.
    Args:
        database: The list of issue dictionaries to save.
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(database, f, indent=4)
