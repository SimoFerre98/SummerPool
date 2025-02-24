import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import config
from data_manager import load_data

def calcola_voti_totali(data_voti):
    voti_totali_calcolati = {}
    for username in data_voti:
        for destinazione, punti in data_voti[username].items():
            voti_totali_calcolati[destinazione] = voti_totali_calcolati.get(destinazione, 0) + punti
    return voti_totali_calcolati

def visualizza_risultati_protetti():
    password_inserita = st.text_input("Password per visualizzare i risultati:", type="password")
    if password_inserita == config.PASSWORD_RISULTATI:
        st.session_state.password_corretta_risultati = True
    elif password_inserita:
        st.error("Password errata. Accesso ai risultati negato.")
        st.session_state.password_corretta_risultati = False
    else:
        st.session_state.password_corretta_risultati = False

    if st.session_state.get('password_corretta_risultati', False):
        st.title("Vediamo un pò dove si và...")

        st.session_state.data = load_data()

        st.header("Risultati Sondaggio")

        voti_totali_attuali = calcola_voti_totali(st.session_state.data["voti"])
        if voti_totali_attuali:
            risultati_df = pd.DataFrame(list(voti_totali_attuali.items()), columns=['Destinazione', 'Punteggio'])
            risultati_df_ordinato = risultati_df.sort_values(by='Punteggio', ascending=False)

            vincitore_punteggio = risultati_df_ordinato['Punteggio'].max()
            vincitori_destinazioni = risultati_df_ordinato[risultati_df_ordinato['Punteggio'] == vincitore_punteggio]['Destinazione'].tolist()

            # *** MODIFICA CHIAVE: RIMOSSO COMPLETAMENTE color=colori_barre ***
            st.bar_chart(risultati_df_ordinato.set_index('Destinazione'), height=400) # Grafico a barre SENZA colori personalizzati

            # *** INIZIO BLOCCO CODICE AGGIUNTO: TESTO VINCITORI SOTTO GRAFICO ***
            st.write(f"**Destinazione/i vincitrice/i:** {', '.join(vincitori_destinazioni)} con {vincitore_punteggio} punti!") # Indica la/le destinazione/i vincitrice/i
            # *** FINE BLOCCO CODICE AGGIUNTO: TESTO VINCITORI SOTTO GRAFICO ***
        else:
            st.info("Nessun voto è stato ancora espresso.")

        st.header("Votanti")
        if st.session_state.data["voti"]:
            voti_lista = []
            for username, voti_utente in st.session_state.data["voti"].items():
                dest_votate = ", ".join(voti_utente.keys())
                voti_lista.append({"Username": username, "Destinazioni Votate": dest_votate})
            voti_df = pd.DataFrame(voti_lista)
            st.dataframe(voti_df)
        else:
            st.info("Ancora nessun voto registrato.")

        st.header("Numero di Persone Votanti")
        num_utenti_votanti = len(st.session_state.data["voti"])
        st.write(f"Voti --> {num_utenti_votanti}")
    elif password_inserita:
        pass
    else:
        st.info("Inserisci la password nel menu laterale per visualizzare i risultati.")

if __name__ == "__main__":
    visualizza_risultati_protetti()