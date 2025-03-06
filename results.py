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

def calcola_frequenze_nuovi_voti(data_voti):
    frequenze = {}
    for username in data_voti:
        for destinazione in data_voti[username]:
            frequenze[destinazione] = frequenze.get(destinazione, 0) + 1
    return frequenze

def visualizza_risultati_protetti():
    st.title("🏖️ Risultati del Sondaggio Vacanze")
    st.session_state.data = load_data()

    # Sezione Risultati Sondaggio Originale
    st.header("📊 Risultati del Sondaggio Originale")
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
            title="Punteggi per Destinazione (Originale)",
            height=400
        )
        fig.update_traces(textposition='auto')
        fig.update_layout(xaxis_title="Destinazioni", yaxis_title="Punteggio Totale", showlegend=False, bargap=0.2)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"**🏆 Destinazione/i vincitrice/i:** {', '.join(vincitori_destinazioni)} con **{vincitore_punteggio} punti**!")
    else:
        st.info("Nessun voto originale è stato ancora espresso.")

    # Sezione Frequenze di Voto Originale
    st.header("📊 Frequenze di Voto per Destinazione (Originale)")
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
            title="Frequenze di Voto per Destinazione (Originale)",
            height=400
        )
        fig_frequenze.update_traces(textposition='auto')
        fig_frequenze.update_layout(xaxis_title="Destinazioni", yaxis_title="Numero di Voti", showlegend=False, bargap=0.2)
        st.plotly_chart(fig_frequenze, use_container_width=True)

        max_frequenza = frequenze_df_ordinato['Frequenza'].max()
        destinazioni_piu_votate = frequenze_df_ordinato[frequenze_df_ordinato['Frequenza'] == max_frequenza]['Destinazione'].tolist()
        st.markdown(f"**🏆 Destinazione/i più votata/e:** {', '.join(destinazioni_piu_votate)} con **{max_frequenza} voti**!")
    else:
        st.info("Nessun voto originale è stato ancora espresso.")

    # Sezione Risultati Nuova Votazione
    st.header("🆕 Risultati della Nuova Votazione")
    utenti_autorizzati = st.session_state.data.get("utenti_autorizzati_nuovi_voti", ["ferre"])  # Default: solo ferre
    if st.session_state.username in utenti_autorizzati:
        nuovi_voti = st.session_state.data.get("nuovi_voti", {})
        if nuovi_voti:
            frequenze_nuovi = calcola_frequenze_nuovi_voti(nuovi_voti)
            df_nuovi = pd.DataFrame(list(frequenze_nuovi.items()), columns=['Destinazione', 'Numero di Voti'])
            df_nuovi_ordinato = df_nuovi.sort_values(by='Numero di Voti', ascending=False)

            fig_nuovi = px.bar(
                df_nuovi_ordinato,
                x='Destinazione',
                y='Numero di Voti',
                color='Destinazione',
                text=df_nuovi_ordinato['Numero di Voti'],
                title="Numero di Voti per Destinazione (Nuova Votazione)",
                height=400
            )
            fig_nuovi.update_traces(textposition='auto')
            fig_nuovi.update_layout(xaxis_title="Destinazioni", yaxis_title="Numero di Voti", showlegend=False, bargap=0.2)
            st.plotly_chart(fig_nuovi, use_container_width=True)

            max_voti = df_nuovi_ordinato['Numero di Voti'].max()
            vincitori = df_nuovi_ordinato[df_nuovi_ordinato['Numero di Voti'] == max_voti]['Destinazione'].tolist()
            st.markdown(f"**🏆 Destinazione/i più votata/e (nuova votazione):** {', '.join(vincitori)} con **{max_voti} voti**!")
        else:
            st.info("Nessun voto è stato ancora espresso nella nuova votazione.")
    else:
        st.warning("I risultati della nuova votazione sono attualmente segreti e visibili solo agli utenti autorizzati.")

    # Sezione Votanti
    st.header("👥 Lista dei Votanti")
    if st.session_state.data["voti"] or st.session_state.data.get("nuovi_voti", {}):
        voti_lista = []
        for username in set(list(st.session_state.data["voti"].keys()) + list(st.session_state.data.get("nuovi_voti", {}).keys())):
            dest_votate = ", ".join(st.session_state.data["voti"].get(username, {}).keys())
            nuovi_voti = ", ".join(st.session_state.data.get("nuovi_voti", {}).get(username, [])) if st.session_state.username in utenti_autorizzati else "Nascosto"
            voti_lista.append({
                "Username": username,
                "Destinazioni Votate (Originale)": dest_votate,
                "Destinazioni Votate (Nuova)": nuovi_voti
            })
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
    num_utenti_nuovi_voti = len(st.session_state.data.get("nuovi_voti", {})) if st.session_state.username in utenti_autorizzati else "Nascosto"
    st.markdown(f"**Numero di persone votanti (originale):** {num_utenti_votanti}")
    st.markdown(f"**Numero di persone votanti (nuova votazione):** {num_utenti_nuovi_voti}")

if __name__ == "__main__":
    visualizza_risultati_protetti()