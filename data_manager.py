import json

# Percorso del file JSON locale
DATABASE_FILE = "database.json"

def load_data():
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("File database.json non trovato. Restituisco dati di default.")
        return {"utenti": {}, "voti": {}, "disponibilita": {}, "nuovi_voti": {}}

def save_data(data):
    """Salva i dati nel file JSON locale."""
    try:
        with open(DATABASE_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("Dati salvati nel file JSON locale.")
    except Exception as e:
        print(f"Errore durante il salvataggio locale: {e}")