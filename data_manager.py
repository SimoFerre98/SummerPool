import sqlite3
import json

DATABASE_FILE = "database.db"

def init_db():
    """Inizializza il database SQLite con una tabella per i dati."""
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS dati (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chiave TEXT UNIQUE,
                    valore TEXT
                )''')
    # Inserisci dati di default se la tabella è vuota
    c.execute("INSERT OR IGNORE INTO dati (chiave, valore) VALUES (?, ?)",
              ("data", json.dumps({"utenti": {}, "voti": {}, "disponibilita": {}, "nuovi_voti": {}, "utenti_autorizzati_nuovi_voti": ["ferre"]})))
    conn.commit()
    conn.close()

def load_data():
    """Carica i dati dal database SQLite."""
    try:
        init_db()  # Assicurati che il database esista
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute("SELECT valore FROM dati WHERE chiave = 'data'")
        result = c.fetchone()
        conn.close()
        if result:
            return json.loads(result[0])
        else:
            print("Nessun dato trovato nel database. Restituisco dati di default.")
            return {"utenti": {}, "voti": {}, "disponibilita": {}, "nuovi_voti": {}, "utenti_autorizzati_nuovi_voti": ["ferre"]}
    except Exception as e:
        print(f"Errore durante il caricamento dal database: {e}")
        return {"utenti": {}, "voti": {}, "disponibilita": {}, "nuovi_voti": {}, "utenti_autorizzati_nuovi_voti": ["ferre"]}

def save_data(data):
    """Salva i dati nel database SQLite."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO dati (chiave, valore) VALUES (?, ?)",
                  ("data", json.dumps(data)))
        conn.commit()
        conn.close()
        print("Dati salvati nel database SQLite.")
    except Exception as e:
        print(f"Errore durante il salvataggio nel database: {e}")