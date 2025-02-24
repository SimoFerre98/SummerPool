import streamlit as st
from data_manager import save_data # Importa la funzione per salvare i dati

def gestisci_avviso_privacy_password():
    st.warning(
        "**Avviso Importante sulla Privacy:** Le password inserite per la registrazione "
        "non sono criptate e vengono memorizzate in chiaro. "
        "Si raccomanda vivamente di **non utilizzare password personali o sensibili** "
        "che usi per altri servizi importanti. "
        "Il creatore di questo sito ha la possibilità tecnica di visualizzare le password inserite."
    )

def gestisci_registrazione():
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
            st.session_state.utente_registrato = True
            st.session_state.username = nuovo_username
            st.session_state.azione_iniziale_selezionata = True
            st.rerun()

def gestisci_login():
    username_login = st.text_input("Username per il login").lower()
    password_login = st.text_input("Password per il login", type="password")
    st.caption("In caso di password dimenticata, contatta l'amministratore del sito.")
    if st.button("Login"):
        if username_login in st.session_state.utenti and st.session_state.utenti[username_login] == password_login:
            st.session_state.utente_registrato = True
            st.session_state.username = username_login
            st.success(f"Login effettuato con successo, benvenuto {username_login}!")
            st.session_state.azione_iniziale_selezionata = True
            st.rerun()
        else:
            st.error("Credenziali non valide. Riprova.")