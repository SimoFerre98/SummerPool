import streamlit as st
import config # Importa config per la password

def visualizza_sezione_risultati():
    sezione_selezionata = st.session_state.get('sezione_selezionata') # Ottieni la sezione selezionata
    if sezione_selezionata == "Risultati":
        password_inserita = st.text_input("Password per visualizzare i risultati:", type="password")
        if password_inserita == config.PASSWORD_RISULTATI: # Usa la password da config.py
            st.session_state.password_corretta_risultati = True
        elif password_inserita:
            st.error("Password errata. Accesso ai risultati negato.")
            st.session_state.password_corretta_risultati = False
    else:
        st.session_state.password_corretta_risultati = False

    if 'password_corretta_risultati' not in st.session_state:
        st.session_state.password_corretta_risultati = False

    if sezione_selezionata == "Risultati":
        if st.session_state.password_corretta_risultati:
            st.header("Codice Sorgente di results.py")
            st.write("Questo è il codice sorgente del file `results.py`...")
            try:
                with open("results.py", "r") as file_results_py:
                    codice_results_py = file_results_py.read()
                    st.code(codice_results_py, language='python')
            except FileNotFoundError:
                st.error("File results.py non trovato...")
        else:
            st.info("Inserisci la password...")