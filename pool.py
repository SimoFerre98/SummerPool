import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import config
import auth
import voting
import details
import results # Importa direttamente il file results.py
import data_manager


if 'utente_registrato' not in st.session_state:
    st.session_state.utente_registrato = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'azione_iniziale_selezionata' not in st.session_state:
    st.session_state.azione_iniziale_selezionata = False
if 'data' not in st.session_state:
    st.session_state.data = data_manager.load_data()
if 'utenti' not in st.session_state:
    st.session_state.utenti = st.session_state.data.get("utenti", {})
if 'voti_totali' not in st.session_state:
    st.session_state.voti_totali = {}
if 'voti_utente' not in st.session_state:
    st.session_state.voti_utente = None
if 'tutti_i_voti' not in st.session_state:
    st.session_state.tutti_i_voti = st.session_state.data.get("voti", {})
if 'destinazioni_selezionate_ordine' not in st.session_state:
    st.session_state.destinazioni_selezionate_ordine = []
if 'password_corretta_risultati' not in st.session_state:
    st.session_state.password_corretta_risultati = False

# *** INIZIO BLOCCO CODICE MODIFICATO: MENU LATERALE - RIMOSSO HAMBURGER ICON - AGGIUNTO LOGOUT BUTTON ***
with st.sidebar:
    st.image("logo.png", width=100) # Logo nel sidebar (opzionale)
    sezione_selezionata = st.selectbox(
        "Menu di Navigazione", # RIMOSSO carattere "☰" - Ora solo testo semplice
        ["Pool di Votazione", "Dettagli Destinazioni", "Risultati"] # Voci del menu
    )
    st.session_state.sezione_selezionata = sezione_selezionata # Salva sezione selezionata in session_state per results_view

    # *** AGGIUNTO BOTTONE LOGOUT NEL MENU LATERALE ***
    if st.session_state.utente_registrato: # Mostra Logout solo se utente è loggato
        if st.button("Logout"):
            st.session_state.utente_registrato = False
            st.session_state.username = ''
            st.session_state.azione_iniziale_selezionata = False
            st.session_state.destinazioni_selezionate_ordine = [] # Resetta la lista delle destinazioni selezionate
            st.session_state.voti_utente = None # Resetta voti utente
            st.success("Logout effettuato con successo.")
            st.rerun()
# *** FINE BLOCCO CODICE MODIFICATO: MENU LATERALE - RIMOSSO HAMBURGER ICON - AGGIUNTO LOGOUT BUTTON ***

# Titolo principale (fuori dal sidebar)
st.title("Sondaggio Destinazioni Vacanze")

# *** INIZIO BLOCCO CODICE AGGIUNTO: TESTO INTRODUTTIVO SIDEBAR ***
st.markdown(
    """
    **Benvenuto al Sondaggio!** 👋
    Per navigare tra le sezioni (Pool di Votazione, Dettagli Destinazioni, Risultati),
    utilizza il menu **"Menu di Navigazione"** situato nel pannello laterale a sinistra.
    _(Se il pannello laterale è chiuso, clicca sull'icona ☰ in alto a sinistra per aprirlo)._
    """
)
# *** FINE BLOCCO CODICE AGGIUNTO: TESTO INTRODUTTIVO SIDEBAR ***


# *** SEZIONE "POOL DI VOTAZIONE" - CHIAMA voting.py ***
if sezione_selezionata == "Pool di Votazione":
    if not st.session_state.utente_registrato:
        auth.gestisci_avviso_privacy_password() # *** SPOSTATO QUI: Avviso privacy solo se NON loggato ***
        azione = st.radio("Seleziona l'azione:", ["Login", "Registrazione"])
        if azione == "Registrazione":
            auth.gestisci_registrazione()
        elif azione == "Login":
            auth.gestisci_login()
    else:
        voting.visualizza_pool_votazione(config.DESTINAZIONI) # Passa la lista delle destinazioni da config.py

# *** SEZIONE "DETTAGLI DESTINAZIONI" - CHIAMA details.py ***
elif sezione_selezionata == "Dettagli Destinazioni":
    details.visualizza_dettagli_destinazioni(config.DESTINAZIONI) # Passa la lista delle destinazioni da config.py

# *** SEZIONE "RISULTATI" - CHIAMA DIRETTAMENTE results.py ***
elif sezione_selezionata == "Risultati":
    results.visualizza_risultati_protetti() # Chiama la funzione in results.py per visualizzare i risultati protetti