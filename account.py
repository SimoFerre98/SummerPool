import streamlit as st
import data_manager

def gestisci_cambio_password():
    """Gestisce il processo di cambio password per l'utente loggato."""
    with st.form(key="cambio_password"):
        vecchia_password = st.text_input("Vecchia password", type="password")
        nuova_password = st.text_input("Nuova password", type="password")
        conferma_password = st.text_input("Conferma nuova password", type="password")
        if st.form_submit_button("Cambia password"):
            utenti = st.session_state.data["utenti"]
            username = st.session_state.username
            if utenti[username]["password"] == vecchia_password:
                if nuova_password == conferma_password:
                    utenti[username]["password"] = nuova_password
                    data_manager.save_data(st.session_state.data)
                    st.success("✅ Password cambiata con successo!")
                else:
                    st.error("❌ Le nuove password non corrispondono!")
            else:
                st.error("❌ Vecchia password errata!")

def visualizza_info_account():
    """Mostra le informazioni dell'account dell'utente loggato."""
    st.write(f"**Username:** {st.session_state.username}")
    # Se hai altre informazioni nell'oggetto utente, puoi aggiungerle qui
    if "data_registrazione" in st.session_state.data["utenti"][st.session_state.username]:
        st.write(f"**Data di registrazione:** {st.session_state.data['utenti'][st.session_state.username]['data_registrazione']}")
    else:
        st.write("**Data di registrazione:** Non disponibile")