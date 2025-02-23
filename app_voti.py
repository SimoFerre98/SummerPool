import streamlit as st
import pandas as pd
import json

DATABASE_FILE = "database.json"

destinazioni = [
    "Cipro", "Ibiza-Formentera", "Mykonos", "Egitto", "Sicilia", "Puglia", "Malta", "Portogallo",
    "Islanda", "Corsica", "Albania", "Montenegro", "Alicante/Benidorm", "Andalucia", "Kos", "Bangkock",
    "Amsterdam/Copenhagen", "Isole Faroe", "Istanbul", "Baku", "Marocco"
]

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
if 'data' not in st.session_state:
    st.session_state.data = load_data()
if 'utenti' not in st.session_state:
    st.session_state.utenti = st.session_state.data.get("utenti", {})
if 'voti_totali' not in st.session_state:
    st.session_state.voti_totali = {} # Non usato più direttamente, calcolato dinamicamente
if 'voti_utente' not in st.session_state:
    st.session_state.voti_utente = None
if 'tutti_i_voti' not in st.session_state:
    st.session_state.tutti_i_voti = st.session_state.data.get("voti", {})

st.title("Sondaggio Destinazioni Vacanze")

if not st.session_state.utente_registrato:
    azione = st.radio("Seleziona l'azione:", ["Login", "Registrazione"])

    if azione == "Registrazione":
        nuovo_username = st.text_input("Username per la registrazione")
        nuova_password = st.text_input("Password per la registrazione", type="password")
        if st.button("Registrati"):
            if nuovo_username in st.session_state.utenti:
                st.error("Username già esistente. Scegli un altro username.")
            else:
                st.session_state.utenti[nuovo_username] = nuova_password
                st.session_state.data["utenti"][nuovo_username] = nuova_password
                st.session_state.data["voti"][nuovo_username] = {} # Inizializza voti utente
                save_data(st.session_state.data)
                st.success("Registrazione completata con successo! Effettua il login.")
    elif azione == "Login":
        username_login = st.text_input("Username per il login")
        password_login = st.text_input("Password per il login", type="password")
        if st.button("Login"):
            if username_login in st.session_state.utenti and st.session_state.utenti[username_login] == password_login:
                st.session_state.utente_registrato = True
                st.session_state.username = username_login
                st.success(f"Login effettuato con successo, benvenuto {username_login}!")
            else:
                st.error("Credenziali non valide. Riprova.")
else:
    st.write(f"Benvenuto, {st.session_state.username}!")

    st.header("Vota le tue 4 destinazioni preferite:")
    destinazioni_selezionate = []
    colonne = st.columns(4)

    for indice, destinazione in enumerate(destinazioni):
        with colonne[indice % 4]:
            if st.checkbox(destinazione, label=destinazione, key=f"dest_{indice}_{st.session_state.username}"):
                destinazioni_selezionate.append(destinazione)

    if len(destinazioni_selezionate) > 4:
        st.warning("Hai selezionato più di 4 destinazioni. Solo le prime 4 saranno considerate per il voto.")
        destinazioni_selezionate = destinazioni_selezionate[:4]

    if st.button("Conferma Voti"):
        if len(destinazioni_selezionate) > 0:
            st.session_state.voti_utente = destinazioni_selezionate

            voti_con_valore = {}
            punti_voto = [4, 3, 2, 1]
            for i, dest in enumerate(destinazioni_selezionate):
                voti_con_valore[dest] = punti_voto[i] if i < 4 else 0

            st.session_state.data["voti"][st.session_state.username] = voti_con_valore
            save_data(st.session_state.data)
            st.success("Voti registrati con successo!")
            del st.session_state.voti_utente # Resetta voti utente in sessione dopo averli salvati
        else:
            st.warning("Seleziona almeno una destinazione prima di confermare.")

    def calcola_voti_totali(data_voti):
        voti_totali_calcolati = {}
        for username in data_voti:
            for destinazione, punti in data_voti[username].items():
                voti_totali_calcolati[destinazione] = voti_totali_calcolati.get(destinazione, 0) + punti
        return voti_totali_calcolati

    st.header("Risultati Sondaggio in Tempo Reale")
    voti_totali_attuali = calcola_voti_totali(st.session_state.data["voti"])
    if voti_totali_attuali:
        risultati_df = pd.DataFrame(list(voti_totali_attuali.items()), columns=['Destinazione', 'Punteggio'])
        risultati_df = risultati_df.sort_values(by='Punteggio', ascending=False)
        st.bar_chart(risultati_df.set_index('Destinazione'))
    else:
        st.info("Nessun voto è stato ancora espresso.")

    st.header("Voti di Tutti gli Utenti")
    if st.session_state.data["voti"]:
        voti_lista = []
        for username, voti_utente in st.session_state.data["voti"].items():
            dest_votate = ", ".join(voti_utente.keys()) # Ottieni solo i nomi delle destinazioni votate
            voti_lista.append({"Username": username, "Destinazioni Votate": dest_votate})
        voti_df = pd.DataFrame(voti_lista)
        st.dataframe(voti_df)
    else:
        st.info("Ancora nessun voto registrato.")


    if st.button("Logout"):
        st.session_state.utente_registrato = False
        st.session_state.username = ''
        st.success("Logout effettuato con successo.")