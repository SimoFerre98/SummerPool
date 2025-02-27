import json
import os
import firebase_admin
from firebase_admin import credentials, db

# Percorso del file JSON locale
DATABASE_FILE = "database.json"

# Funzione per inizializzare Firebase (se configurato)
def init_firebase():
    try:
        # Carica le credenziali da file o da variabili d'ambiente
        cred_path = "firebase_credentials.json"
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://your-project-id.firebaseio.com/'  # Sostituisci con il tuo URL
            })
            return True
        else:
            print("Credenziali Firebase non trovate. Uso il file JSON locale.")
            return False
    except Exception as e:
        print(f"Errore nell'inizializzazione di Firebase: {e}")
        return False

# Inizializza Firebase all'avvio (se possibile)
firebase_initialized = init_firebase()

def load_data():
    """Carica i dati da Firebase se disponibile, altrimenti dal file JSON locale."""
    if firebase_initialized:
        try:
            ref = db.reference('/')
            data = ref.get()
            if data is not None:
                print("Dati caricati da Firebase.")
                return data
            else:
                print("Nessun dato su Firebase. Carico dal file JSON locale.")
        except Exception as e:
            print(f"Errore nel caricamento da Firebase: {e}")
    
    # Fallback: carica dal file JSON locale (comportamento originale)
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"utenti": {}, "voti": {}, "disponibilita": {}}

def save_data(data):
    """Salva i dati su Firebase se disponibile, altrimenti sul file JSON locale."""
    if firebase_initialized:
        try:
            ref = db.reference('/')
            ref.set(data)
            print("Dati salvati su Firebase.")
            return
        except Exception as e:
            print(f"Errore nel salvataggio su Firebase: {e}")
    
    # Fallback: salva sul file JSON locale (comportamento originale)
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Dati salvati sul file JSON locale.")