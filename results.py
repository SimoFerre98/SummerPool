import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import config # Importa il file di configurazione

DATABASE_FILE = "database.json" # Assicurati che sia lo stesso nome file di pool.py

def load_data(): # Copia ANCHE la funzione load_data da pool.py
    try:
        with open(DATABASE_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"utenti": {}, "voti": {}}
    return data

def calcola_voti_totali(data_voti):
    voti_totali_calcolati = {}
    for username in data_voti:
        for destinazione, punti in data_voti[username].items():
            voti_totali_calcolati[destinazione] = voti_totali_calcolati.get(destinazione, 0) + punti
    return voti_totali_calcolati

def visualizza_risultati_protetti(): # NUOVA funzione per gestire password e visualizzazione
    password_inserita = st.text_input("Password per visualizzare i risultati:", type="password")
    if password_inserita == config.PASSWORD_RISULTATI: # Usa la password da config.py
        st.session_state.password_corretta_risultati = True
    elif password_inserita:
        st.error("Password errata. Accesso ai risultati negato.")
        st.session_state.password_corretta_risultati = False
    else: # Caso in cui non è stata inserita la password
        st.session_state.password_corretta_risultati = False

    if st.session_state.get('password_corretta_risultati', False): # Controlla se la password è corretta (usando get per evitare errori se non inizializzato)
        st.title("Risultati Sondaggio Destinazioni Vacanze (Visualizzazione Riservata)") # Titolo per results.py

        st.session_state.data = load_data() # Carica i dati in results.py, come fai in pool.py

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

        st.header("Utenti che hanno votato") # Copia ANCHE la sezione "Utenti che hanno votato" da pool.py (opzionale, se vuoi mostrarla anche qui)
        num_utenti_votanti = len(st.session_state.data["voti"])
        st.write(f"Numero di utenti che hanno espresso il loro voto: {num_utenti_votanti}")
    elif password_inserita: # Se la password è stata inserita ma non è corretta
        pass # L'errore è già gestito sopra nella condizione elif password_inserita == config.PASSWORD_RISULTATI:
    else: # Se non è stata inserita la password (e non è corretta, condizione implicita)
        st.info("Inserisci la password nel menu laterale per visualizzare i risultati.")


if __name__ == "__main__": # Solo se results.py viene eseguito direttamente (per test locali)
    visualizza_risultati_protetti() # Chiama la funzione per visualizzare i risultati protetti