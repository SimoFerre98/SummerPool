import json
import firebase_admin
from firebase_admin import credentials, db

# Percorso del file JSON locale
DATABASE_FILE = "database.json"

# Funzione per caricare i dati dal file JSON locale
def load_local_data():
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Errore: Il file {DATABASE_FILE} non è stato trovato.")
        return None

# Funzione per pulire le chiavi non valide
def clean_keys(data):
    if isinstance(data, dict):
        return {clean_key(k): clean_keys(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_keys(item) for item in data]
    else:
        return data

def clean_key(key):
    """Rimuove o sostituisce caratteri non validi per Firebase."""
    if not key:  # Gestisce chiavi vuote
        return "empty_key"
    return key.replace('$', '_').replace('#', '_').replace('[', '_').replace(']', '_').replace('/', '_').replace('.', '_')

# Funzione per inizializzare Firebase
def init_firebase():
    try:
        cred = credentials.Certificate("firebase_credentials.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://summerpool-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        print("Firebase inizializzato con successo.")
        return True
    except Exception as e:
        print(f"Errore nell'inizializzazione di Firebase: {e}")
        return False

# Funzione per salvare i dati su Firebase
def save_to_firebase(data):
    try:
        ref = db.reference('/')
        ref.set(data)
        print("Dati salvati con successo su Firebase.")
    except Exception as e:
        print(f"Errore nel salvataggio su Firebase: {e}")

# Script principale
if __name__ == "__main__":
    # Carica i dati dal file JSON locale
    data = load_local_data()
    if data is not None:
        # Pulisci i dati
        cleaned_data = clean_keys(data)
        # Inizializza Firebase
        if init_firebase():
            # Salva i dati su Firebase
            save_to_firebase(cleaned_data)
        else:
            print("Firebase non è stato inizializzato correttamente.")
    else:
        print("Impossibile procedere senza dati locali.")