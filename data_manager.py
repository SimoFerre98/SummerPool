import json
import threading
import firebase_admin
from firebase_admin import credentials, db
import streamlit as st
import tempfile
import os

# Percorso del file JSON locale
DATABASE_FILE = "database.json"

# Recupera i segreti da Streamlit
firebase_secrets = st.secrets["firebase"]

# Crea un file temporaneo con le credenziali
with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
    json.dump(firebase_secrets, temp_file)  # Scrivi il dizionario nel file
    temp_file_path = temp_file.name

# Inizializza Firebase usando il percorso del file temporaneo
cred = credentials.Certificate(temp_file_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://summerpool-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Pulisci rimuovendo il file temporaneo
os.remove(temp_file_path)

def load_data():
    """Carica i dati dal file JSON locale."""
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"utenti": {}, "voti": {}, "disponibilita": {}}

def save_data(data):
    """Salva i dati nel file JSON locale e su Firebase in modo asincrono."""
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Dati salvati nel file JSON locale.")
    threading.Thread(target=save_to_firebase, args=(data,)).start()

def save_to_firebase(data):
    """Salva i dati su Firebase in un thread separato."""
    try:
        ref = db.reference('/')
        ref.set(data)
        print("Dati sincronizzati con successo su Firebase.")
    except Exception as e:
        print(f"Errore nel salvataggio su Firebase: {type(e).__name__}: {str(e)}")