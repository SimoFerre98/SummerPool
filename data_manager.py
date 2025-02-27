import json
import threading
import firebase_admin
from firebase_admin import credentials, db

# Percorso del file JSON locale
DATABASE_FILE = "database.json"

# Inizializzazione di Firebase
try:
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://summerpool-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    print("Firebase inizializzato con successo.")
except Exception as e:
    print(f"Errore durante l'inizializzazione di Firebase: {e}")

def load_data():
    """Carica i dati dal file JSON locale."""
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("File database.json non trovato. Restituisco dati di default.")
        return {"utenti": {}, "voti": {}, "disponibilita": {}}

def save_data(data):
    """Salva i dati nel file JSON locale e su Firebase in modo asincrono."""
    try:
        with open(DATABASE_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print("Dati salvati nel file JSON locale.")
    except Exception as e:
        print(f"Errore durante il salvataggio locale: {e}")
    
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