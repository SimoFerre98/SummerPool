import streamlit as st
import pandas as pd
import plotly.express as px
from data_manager import load_data

def calcola_voti_totali(data_voti):
    voti_totali_calcolati = {}
    for username in data_voti:
        for destinazione, punti in data_voti[username].items():
            voti_totali_calcolati[destinazione] = voti_totali_calcolati.get(destinazione, 0) + punti
    return voti_totali_calcolati

def calcola_frequenze_voto(data_voti):
    frequenze = {}
    for username in data_voti:
        for destinazione in data_voti[username].keys():
            frequenze[destinazione] = frequenze.get(destinazione, 0) + 1
    return frequenze

def visualizza_risultati_protetti():
    st.title("🏖️ Risultati del Sondaggio Vacanze")
    st.session_state.data = load_data()

    # Sezione Risultati Sondaggio (grafico dei punteggi totali)
    st.header("📊 Risultati del Sondaggio")
    voti_totali_attuali = calcola_voti_totali(st.session_state.data["voti"])

    if voti_totali_attuali:
        risultati_df = pd.DataFrame(list(voti_totali_attuali.items()), columns=['Destinazione', 'Punteggio'])
        risultati_df_ordinato = risultati_df.sort_values(by='Punteggio', ascending=False)

        vincitore_punteggio = risultati_df_ordinato['Punteggio'].max()
        vincitori_destinazioni = risultati_df_ordinato[risultati_df_ordinato['Punteggio'] == vincitore_punteggio]['Destinazione'].tolist()

        fig = px.bar(
            risultati_df_ordinato,
            x='Destinazione',
            y='Punteggio',
            color='Destinazione',
            text=risultati_df_ordinato['Punteggio'],
            title="Punteggi per Destinazione",
            height=400
        )
        fig.update_traces(textposition='auto')
        fig.update_layout(
            xaxis_title="Destinazioni",
            yaxis_title="Punteggio Totale",
            showlegend=False,
            bargap=0.2
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"**🏆 Destinazione/i vincitrice/i:** {', '.join(vincitori_destinazioni)} con **{vincitore_punteggio} punti**!")
    else:
        st.info("Nessun voto è stato ancora espresso.")

    # Nuova sezione: Frequenze di Voto
    st.header("📊 Frequenze di Voto per Destinazione")
    frequenze_voto = calcola_frequenze_voto(st.session_state.data["voti"])

    if frequenze_voto:
        frequenze_df = pd.DataFrame(list(frequenze_voto.items()), columns=['Destinazione', 'Frequenza'])
        frequenze_df_ordinato = frequenze_df.sort_values(by='Frequenza', ascending=False)

        fig_frequenze = px.bar(
            frequenze_df_ordinato,
            x='Destinazione',
            y='Frequenza',
            color='Destinazione',
            text=frequenze_df_ordinato['Frequenza'],
            title="Frequenze di Voto per Destinazione",
            height=400
        )
        fig_frequenze.update_traces(textposition='auto')
        fig_frequenze.update_layout(
            xaxis_title="Destinazioni",
            yaxis_title="Numero di Voti",
            showlegend=False,
            bargap=0.2
        )
        st.plotly_chart(fig_frequenze, use_container_width=True)

        max_frequenza = frequenze_df_ordinato['Frequenza'].max()
        destinazioni_piu_votate = frequenze_df_ordinato[frequenze_df_ordinato['Frequenza'] == max_frequenza]['Destinazione'].tolist()
        st.markdown(f"**🏆 Destinazione/i più votata/e:** {', '.join(destinazioni_piu_votate)} con **{max_frequenza} voti**!")
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

        st.dataframe(
            voti_df.style.set_properties(**{
                'background-color': '#f9f9f9',
                'border-color': '#dddddd',
                'padding': '5px',
                'text-align': 'left'
            }).set_table_styles([{
                'selector': 'th',
                'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]
            }]),
            use_container_width=True
        )
    else:
        st.info("Ancora nessun voto registrato.")

    # Sezione Statistiche
    st.header("📈 Statistiche")
    num_utenti_votanti = len(st.session_state.data["voti"])
    st.markdown(f"**Numero di persone votanti:** {num_utenti_votanti}")

if __name__ == "__main__":
    visualizza_risultati_protetti()