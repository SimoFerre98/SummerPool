import streamlit as st
from data_manager import save_data  # Importa la funzione per salvare i dati

def gestisci_avviso_privacy_password():
    st.warning(
        "**Avviso Importante sulla Privacy:** Le password inserite per la registrazione "
        "non sono criptate e vengono memorizzate in chiaro. "
        "Si raccomanda vivamente di **non utilizzare password personali o sensibili** "
        "che usi per altri servizi importanti. "
        "Il creatore di questo sito ha la possibilità tecnica di visualizzare le password inserite."
    )

def gestisci_registrazione():
    st.subheader("Registrazione Nuovo Utente")
    username_registrazione = st.text_input("Username per la registrazione:")
    password_registrazione = st.text_input("Password per la registrazione:", type="password")

    if st.button("Registrati"):
        if username_registrazione and password_registrazione:
            utenti_esistenti = st.session_state.data.get("utenti", {})
            if username_registrazione in utenti_esistenti:
                st.error("Username già esistente. Scegli un altro username.")
            else:
                # Salva i dati dell'utente
                st.session_state.data["utenti"][username_registrazione] = {"password": password_registrazione}
                st.session_state.utenti = st.session_state.data["utenti"]
                save_data(st.session_state.data)
                
                # Effettua il login automaticamente
                st.session_state.utente_registrato = True
                st.session_state.username = username_registrazione
                st.session_state.azione_iniziale_selezionata = True
                st.session_state.sezione_selezionata = "Pool di Votazione"  # Imposta la sezione votazioni
                
                st.success(f"Utente '{username_registrazione}' registrato e loggato con successo!")
                print(f"Nuovo utente registrato e loggato: Username='{username_registrazione}'")
                
                # Ricarica la pagina per mostrare la sezione votazioni
                st.rerun()
        else:
            st.warning("Username e password sono obbligatori per la registrazione.")

def gestisci_login():
    st.subheader("Login Utente Registrato")
    username_login = st.text_input("Username per il login:")
    password_login = st.text_input("Password per il login:", type="password")
    st.caption("In caso di password dimenticata, contatta l'amministratore del sito.")
    if st.button("Login"):
        if username_login and password_login:
            utenti_esistenti = st.session_state.data.get("utenti", {})
            utente_data = utenti_esistenti.get(username_login)
            if utente_data and utente_data.get("password") == password_login:
                st.session_state.utente_registrato = True
                st.session_state.username = username_login
                st.session_state.azione_iniziale_selezionata = True
                st.session_state.sezione_selezionata = "Pool di Votazione"  # Imposta la sezione votazioni
                st.success(f"Login effettuato con successo per l'utente '{username_login}'!")
                print(f"Utente loggato: Username='{username_login}'")
                st.rerun()
            else:
                st.error("Credenziali non valide. Riprova.")
        else:
            st.warning("Username e password sono obbligatori per il login.")