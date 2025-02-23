import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt # Anche se non lo usiamo più, per ora lasciamolo, rimuoveremo importazioni inutilizzate alla fine

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
if 'azione_iniziale_selezionata' not in st.session_state: # Nuovo stato per azione iniziale
    st.session_state.azione_iniziale_selezionata = False # Flag per evitare loop di renderizzazione
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

# Aggiungi il logo qui
st.image("logo.png", width=100)

st.title("Sondaggio Destinazioni Vacanze")

if not st.session_state.utente_registrato:
    # Mostra sempre "Login" e "Registrazione" come prima azione
    azione = st.radio("Seleziona l'azione:", ["Login", "Registrazione"]) # Nessun valore predefinito impostato, il primo sarà selezionato di default

    if azione == "Registrazione":
        nuovo_username = st.text_input("Username per la registrazione").lower()
        nuova_password = st.text_input("Password per la registrazione", type="password")
        if st.button("Registrati"): # Bottone di registrazione, azione singola
            if nuovo_username in st.session_state.utenti:
                st.error("Username già esistente. Scegli un altro username.")
            else:
                st.session_state.utenti[nuovo_username] = nuova_password
                st.session_state.data["utenti"][nuovo_username] = nuova_password
                st.session_state.data["voti"][nuovo_username] = {}
                save_data(st.session_state.data)
                st.success("Registrazione completata con successo! Effettua il login.")
                st.session_state.azione_iniziale_selezionata = True # Imposta il flag per evitare loop
                st.experimental_rerun() # Rerunning per aggiornare la UI dopo la registrazione
    elif azione == "Login":
        username_login = st.text_input("Username per il login").lower()
        password_login = st.text_input("Password per il login", type="password")
        if st.button("Login"): # Bottone di login, azione singola
            if username_login in st.session_state.utenti and st.session_state.utenti[username_login] == password_login:
                st.session_state.utente_registrato = True
                st.session_state.username = username_login
                st.success(f"Login effettuato con successo, benvenuto {username_login}!")
                st.session_state.azione_iniziale_selezionata = True # Imposta il flag per evitare loop
                st.experimental_rerun() # Rerunning per aggiornare la UI dopo il login
            else:
                st.error("Credenziali non valide. Riprova.")
else:
    st.write(f"Benvenuto, {st.session_state.username}!")

    st.header("Vota le tue 4 destinazioni preferite:")
    destinazioni_selezionate = []
    colonne = st.columns(4)
    punti_voto_assegnati = {}

    # Carica i voti precedenti dell'utente, se esistono
    voti_precedenti = st.session_state.data["voti"].get(st.session_state.username, {})
    destinazioni_votate_precedentemente = list(voti_precedenti.keys())

    punti_disponibili = [4, 3, 2, 1]

    for indice, destinazione in enumerate(destinazioni):
        with colonne[indice % 4]:
            default_value = destinazione in destinazioni_votate_precedentemente
            checkbox_key = f"dest_{indice}_{st.session_state.username}"
            checkbox_value = st.checkbox(destinazione, key=checkbox_key, value=default_value)

            if checkbox_value:
                destinazioni_selezionate.append(destinazione)

    if len(destinazioni_selezionate) > 4:
        st.warning("Hai selezionato più di 4 destinazioni. Solo le prime 4 saranno considerate per il voto.")
        destinazioni_selezionate = destinazioni_selezionate[:4]

    # Assegna i punti alle destinazioni selezionate in base all'ordine di selezione
    punti_voto_assegnati = {}
    for i, destinazione in enumerate(destinazioni_selezionate):
        if i < 4:
            punti_voto_assegnati[destinazione] = punti_disponibili[i]

    # Mostra le destinazioni selezionate con i punti accanto
    if destinazioni_selezionate:
        st.write("Destinazioni selezionate e punti:")
        for i, destinazione in enumerate(destinazioni_selezionate):
            punti = punti_voto_assegnati.get(destinazione, 0)
            st.write(f"- {destinazione} ({punti} punti)")


    if st.button("Conferma Voti"): # Bottone di conferma voti, azione singola
        if len(destinazioni_selezionate) > 0:
            st.session_state.voti_utente = destinazioni_selezionate

            voti_con_valore = punti_voto_assegnati

            st.session_state.data["voti"][st.session_state.username] = voti_con_valore
            save_data(st.session_state.data)
            st.success("Voti registrati con successo!")
            del st.session_state.voti_utente
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
            dest_votate = ", ".join(voti_utente.keys())
            voti_lista.append({"Username": username, "Destinazioni Votate": dest_votate})
        voti_df = pd.DataFrame(voti_lista)
        st.dataframe(voti_df)
    else:
        st.info("Ancora nessun voto registrato.")

    # Rimossa la sezione del grafico a torta "Partecipazione al Voto"

    st.header("Utenti che hanno votato") # Mantiene la sezione con il numero utenti votanti
    num_utenti_votanti = len(st.session_state.data["voti"])
    st.write(f"Numero di utenti che hanno espresso il loro voto: {num_utenti_votanti}")

    if st.button("Logout"): # Bottone logout, azione singola
        st.session_state.utente_registrato = False
        st.session_state.username = ''
        st.success("Logout effettuato con successo.")
        st.session_state.azione_iniziale_selezionata = True # Imposta il flag per evitare loop
        st.experimental_rerun() # Rerunning per aggiornare la UI dopo il logout