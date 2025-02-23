import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

DATABASE_FILE = "database.json"

# Ordina le destinazioni alfabeticamente
destinazioni = [
    "Albania", "Alicante/Benidorm", "Amsterdam/Copenhagen", "Andalucia", "Baku", "Bangkock", "Corsica",
    "Cipro", "Egitto", "Ibiza-Formentera", "Islanda", "Isole Faroe", "Istanbul", "Kos", "Malta",
    "Marocco", "Montenegro", "Mykonos", "Portogallo", "Puglia", "Sicilia"
]
destinazioni.sort() # Ordina la lista in-place

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

if 'utente_registrato' not in st.session_state:
    st.session_state.utente_registrato = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'azione_iniziale_selezionata' not in st.session_state:
    st.session_state.azione_iniziale_selezionata = False
if 'data' not in st.session_state:
    st.session_state.data = load_data()
if 'utenti' not in st.session_state:
    st.session_state.utenti = st.session_state.data.get("utenti", {})
if 'voti_totali' not in st.session_state:
    st.session_state.voti_totali = {}
if 'voti_utente' not in st.session_state:
    st.session_state.voti_utente = None
if 'tutti_i_voti' not in st.session_state:
    st.session_state.tutti_i_voti = st.session_state.data.get("voti", {})
if 'destinazioni_selezionate_ordine' not in st.session_state:
    st.session_state.destinazioni_selezionate_ordine = [] # Inizializzazione lista ordinata

# Aggiungi il logo qui
st.image("logo.png", width=100)

st.title("Sondaggio Destinazioni Vacanze")

if not st.session_state.utente_registrato:
    # **INIZIO BLOCCO CODICE INSERITO: AVVISO PRIVACY PASSWORD**
    st.warning(
        "**Avviso Importante sulla Privacy:** Le password inserite per la registrazione "
        "non sono criptate e vengono memorizzate in chiaro. "
        "Si raccomanda vivamente di **non utilizzare password personali o sensibili** "
        "che usi per altri servizi importanti. "
        "Il creatore di questo sito ha la possibilità tecnica di visualizzare le password inserite."
    )
    # **FINE BLOCCO CODICE INSERITO: AVVISO PRIVACY PASSWORD**

    azione = st.radio("Seleziona l'azione:", ["Login", "Registrazione"])

    if azione == "Registrazione":
        nuovo_username = st.text_input("Username per la registrazione").lower()
        nuova_password = st.text_input("Password per la registrazione", type="password")
        if st.button("Registrati"):
            if nuovo_username in st.session_state.utenti:
                st.error("Username già esistente. Scegli un altro username.")
            else:
                st.session_state.utenti[nuovo_username] = nuova_password
                st.session_state.data["utenti"][nuovo_username] = nuova_password
                st.session_state.data["voti"][nuovo_username] = {}
                save_data(st.session_state.data)
                st.success("Registrazione completata con successo! Effettua il login.")
                st.session_state.azione_iniziale_selezionata = True
                st.rerun()
    elif azione == "Login":
        username_login = st.text_input("Username per il login").lower()
        password_login = st.text_input("Password per il login", type="password")
        if st.button("Login"):
            if username_login in st.session_state.utenti and st.session_state.utenti[username_login] == password_login:
                st.session_state.utente_registrato = True
                st.session_state.username = username_login
                st.success(f"Login effettuato con successo, benvenuto {username_login}!")
                st.session_state.azione_iniziale_selezionata = True
                st.rerun()
            else:
                st.error("Credenziali non valide. Riprova.")
else:
    st.write(f"Benvenuto, {st.session_state.username}!")
    # **INIZIO BLOCCO CODICE INSERITO: ISTRUZIONI VOTAZIONE**
    st.info(
        "**Come funziona la votazione:** Seleziona fino a 4 destinazioni che preferisci. "
        "La **prima destinazione** che selezioni riceverà **4 punti**, la **seconda 3 punti**, "
        "la **terza 2 punti** e la **quarta 1 punto**. "
        "Se selezioni più di 4 destinazioni, verranno considerate solo le prime 4 in ordine di selezione."
    )
    # **FINE BLOCCO CODICE INSERITO: ISTRUZIONI VOTAZIONE**

    st.header("Vota le tue 4 destinazioni preferite:")
    destinazioni_selezionate = [] # RIMOSSA - Usa st.session_state.destinazioni_selezionate_ordine
    punti_voto_assegnati = {}
    colonne = st.columns(4)
    punti_disponibili = [4, 3, 2, 1]

    # Carica i voti precedenti dell'utente, se esistono
    voti_precedenti = st.session_state.data["voti"].get(st.session_state.username, {})
    destinazioni_votate_precedentemente = list(voti_precedenti.keys())


    for indice, destinazione in enumerate(destinazioni):
        with colonne[indice % 4]:
            default_value = destinazione in destinazioni_votate_precedentemente
            checkbox_key = f"dest_{indice}_{destinazione}"
            checkbox_value = st.checkbox(destinazione, key=checkbox_key, value=default_value)

            if checkbox_value:
                # Se la checkbox è selezionata:
                if destinazione not in st.session_state.destinazioni_selezionate_ordine:
                    # Aggiungi alla lista ORDINATA SOLO se non è già presente
                    st.session_state.destinazioni_selezionate_ordine.append(destinazione)
            else:
                # Se la checkbox è DESELEZIONATA:
                if destinazione in st.session_state.destinazioni_selezionate_ordine:
                    # Rimuovi dalla lista ORDINATA se presente
                    st.session_state.destinazioni_selezionate_ordine.remove(destinazione)

    # Usa la lista ORDINATA da session_state per le operazioni successive
    destinazioni_selezionate = st.session_state.destinazioni_selezionate_ordine


    if len(destinazioni_selezionate) > 4:
        st.warning("Hai selezionato più di 4 destinazioni. Solo le prime 4 saranno considerate per il voto.")
        destinazioni_selezionate = destinazioni_selezionate[:4]

    # Assegna i punti ALLE DESTINAZIONI SELEZIONATE in base all'ordine DI SELEZIONE
    punti_voto_assegnati = {}
    for i, destinazione in enumerate(destinazioni_selezionate):
        if i < 4:
            punti_voto_assegnati[destinazione] = punti_disponibili[i]


    # RIPRISTINO visualizzazione elenco puntato sotto i checkbox:
    if destinazioni_selezionate:
        st.write("Destinazioni selezionate e punti:")
        for i, destinazione in enumerate(destinazioni_selezionate):
            punti = punti_voto_assegnati.get(destinazione, 0)
            st.write(f"- {destinazione} ({punti} punti)")


    if st.button("Conferma Voti"):
        if len(destinazioni_selezionate) > 0:
            st.session_state.voti_utente = destinazioni_selezionate

            voti_con_valore = punti_voto_assegnati

            st.session_state.data["voti"][st.session_state.username] = voti_con_valore
            save_data(st.session_state.data)
            st.success("Voti registrati con successo!")
            del st.session_state.voti_utente
        else:
            st.warning("Seleziona almeno una destinazione prima di confermare.")

    # La sezione per il link a results.py è stata RIMOSSA da qui