import json
import threading
import firebase_admin
from firebase_admin import credentials, db

# Percorso del file JSON locale
DATABASE_FILE = "database.json"

# Inizializzazione di Firebase (eseguita sempre all'avvio)
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://summerpool-default-rtdb.europe-west1.firebasedatabase.app/'
})

def load_data():
    """Carica i dati dal file JSON locale."""
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"utenti": {}, "voti": {}, "disponibilita": {}}

def save_data(data):
    """Salva i dati nel file JSON locale e su Firebase in modo asincrono."""
    # Salva i dati nel file JSON locale
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Dati salvati nel file JSON locale.")

    # Salva su Firebase in modo asincrono
    threading.Thread(target=save_to_firebase, args=(data,)).start()

def save_to_firebase(data):
    """Salva i dati su Firebase in un thread separato."""
    try:
        ref = db.reference('/')
        ref.set(data)
        print("Dati sincronizzati con successo su Firebase.")
    except Exception as e:
        print(f"Errore nel salvataggio su Firebase: {type(e).__name__}: {str(e)}")