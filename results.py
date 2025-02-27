import streamlit as st
import pandas as pd
import plotly.express as px  # Sostituiamo matplotlib con plotly per grafici interattivi
from data_manager import load_data

def calcola_voti_totali(data_voti):
    voti_totali_calcolati = {}
    for username in data_voti:
        for destinazione, punti in data_voti[username].items():
            voti_totali_calcolati[destinazione] = voti_totali_calcolati.get(destinazione, 0) + punti
    return voti_totali_calcolati

def visualizza_risultati_protetti():
    # Titolo con un tocco di stile
    st.title("🏖️ Risultati del Sondaggio Vacanze")

    # Carica i dati
    st.session_state.data = load_data()

    # Sezione Risultati Sondaggio
    st.header("📊 Risultati del Sondaggio")
    voti_totali_attuali = calcola_voti_totali(st.session_state.data["voti"])

    if voti_totali_attuali:
        # Crea un DataFrame per i risultati
        risultati_df = pd.DataFrame(list(voti_totali_attuali.items()), columns=['Destinazione', 'Punteggio'])
        risultati_df_ordinato = risultati_df.sort_values(by='Punteggio', ascending=False)

        # Determina il vincitore
        vincitore_punteggio = risultati_df_ordinato['Punteggio'].max()
        vincitori_destinazioni = risultati_df_ordinato[risultati_df_ordinato['Punteggio'] == vincitore_punteggio]['Destinazione'].tolist()

        # Grafico interattivo con Plotly
        fig = px.bar(
            risultati_df_ordinato,
            x='Destinazione',
            y='Punteggio',
            color='Destinazione',  # Colori diversi per ogni barra
            text=risultati_df_ordinato['Punteggio'],  # Mostra i punteggi sulle barre
            title="Punteggi per Destinazione",
            height=400
        )
        fig.update_traces(textposition='auto')  # Posiziona il testo automaticamente
        fig.update_layout(
            xaxis_title="Destinazioni",
            yaxis_title="Punteggio Totale",
            showlegend=False,  # Nasconde la legenda (ridondante con i colori)
            bargap=0.2  # Spazio tra le barre
        )
        st.plotly_chart(fig, use_container_width=True)

        # Evidenzia il vincitore
        st.markdown(f"**🏆 Destinazione/i vincitrice/i:** {', '.join(vincitori_destinazioni)} con **{vincitore_punteggio} punti**!")
    else:
        st.info("Nessun voto è stato ancora espresso.")

    # Sezione Votanti
    st.header("👥 Lista dei Votanti")
    if st.session_state.data["voti"]:
        voti_lista = []
        for username, voti_utente in st.session_state.data["voti"].items():
            dest_votate = ", ".join(voti_utente.keys())
            voti_lista.append({"Username": username, "Destinazioni Votate": dest_votate})
        voti_df = pd.DataFrame(voti_lista)

        # Stile per la tabella
        st.dataframe(
            voti_df.style.set_properties(**{
                'background-color': '#f9f9f9',
                'border-color': '#dddddd',
                'padding': '5px',
                'text-align': 'left'
            }).set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]}
            ]),
            use_container_width=True
        )
    else:
        st.info("Ancora nessun voto registrato.")

    # Sezione Numero di Votanti
    st.header("📈 Statistiche")
    num_utenti_votanti = len(st.session_state.data["voti"])
    st.markdown(f"**Numero di persone votanti:** {num_utenti_votanti}")

if __name__ == "__main__":
    visualizza_risultati_protetti()