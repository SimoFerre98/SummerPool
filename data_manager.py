import json

DATABASE_FILE = "database.json" # Potremmo importare DATABASE_FILE da config.py, ma per semplicità lo ridefiniamo qui o importiamo config e usiamo config.DATABASE_FILE

def load_data():
    try:
        with open(DATABASE_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"utenti": {}, "voti": {}}
    return data

def save_data(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)