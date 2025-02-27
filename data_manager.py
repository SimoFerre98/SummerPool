import json

def load_data():
    try:
        with open("database.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"utenti": {}, "voti": {}, "disponibilita": {}}

def save_data(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent=4)