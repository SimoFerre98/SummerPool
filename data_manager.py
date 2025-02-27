import json
import os
import threading
import firebase_admin
from firebase_admin import credentials, db

# Percorso del file JSON locale
DATABASE_FILE = "database.json"

# Funzione per inizializzare Firebase
def init_firebase():
    try:
        # Carica le credenziali da un file
        cred_path = "firebase_credentials.json"
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://summerpool-default-rtdb.europe-west1.firebasedatabase.app/'
            })
            return True
        else:
            print("Credenziali Firebase non trovate. Uso solo il file JSON locale.")
            return False
    except Exception as e:
        print(f"Errore nell'inizializzazione di Firebase: {e}")
        return False

# Inizializza Firebase all'avvio (se possibile)
firebase_initialized = init_firebase()

def load_data():
    """Carica i dati dal file JSON locale."""
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"utenti": {}, "voti": {}, "disponibilita": {}}

def save_data(data):
    """Salva i dati nel file JSON locale e, se configurato, su Firebase in modo asincrono."""
    # Salva i dati nel file JSON locale
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Dati salvati nel file JSON locale.")

    # Se Firebase è configurato, salva su Firebase in modo asincrono
    if firebase_initialized:
        threading.Thread(target=save_to_firebase, args=(data,)).start()

def save_to_firebase(data):
    """Salva i dati su Firebase in un thread separato."""
    try:
        ref = db.reference('/')
        ref.set(data)
        print("Dati salvati su Firebase.")
    except Exception as e:
        print(f"Errore nel salvataggio su Firebase: {e}")