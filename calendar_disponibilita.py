import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import data_manager

def visualizza_calendario_disponibilita():
    if not st.session_state.utente_registrato:
        st.warning("🚫 Devi effettuare il login per inserire le tue disponibilità!")
        return

    # Titolo accattivante
    st.title("🗓️ Calendario Disponibilità Vacanze")

    # Carica i dati esistenti
    data = st.session_state.data
    if "disponibilita" not in data:
        data["disponibilita"] = {}

    # Utente corrente
    utente_corrente = st.session_state.username
    utenti_registrati = list(data["utenti"].keys())
    colori = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD', '#D4A5A5', '#9B59B6', '#3498DB', 
              '#E74C3C', '#2ECC71', '#F1C40F', '#8E44AD']  # Espanso a 12 colori, può essere ulteriormente ampliato

    # Sezione per inserire nuove disponibilità
    st.subheader("➕ Aggiungi la tua disponibilità")
    with st.form(key='form_disponibilita'):
        col1, col2 = st.columns(2)
        with col1:
            data_inizio = st.date_input("Data inizio", key="inizio")
        with col2:
            data_fine = st.date_input("Data fine", key="fine")
        submit_button = st.form_submit_button(label="Aggiungi")

    if submit_button:
        if data_inizio > data_fine:
            st.error("❌ La data di inizio deve essere precedente alla data di fine!")
        else:
            if utente_corrente not in data["disponibilita"]:
                data["disponibilita"][utente_corrente] = []
            data["disponibilita"][utente_corrente].append((data_inizio.strftime('%Y-%m-%d'), data_fine.strftime('%Y-%m-%d')))
            data_manager.save_data(data)
            st.session_state.data = data
            st.success(f"✅ Disponibilità aggiunta per {utente_corrente}!")

    # Sezione per visualizzare, modificare ed eliminare le disponibilità personali
    st.subheader(f"📋 Le tue disponibilità, {utente_corrente}")
    if utente_corrente in data["disponibilita"] and data["disponibilita"][utente_corrente]:
        disponibilita_personali = data["disponibilita"][utente_corrente]
        for i, (inizio, fine) in enumerate(disponibilita_personali):
            with st.expander(f"Periodo {i+1}: {inizio} - {fine}", expanded=False):
                col_mod, col_del = st.columns([3, 1])
                with col_mod:
                    if st.button(f"Modifica", key=f"mod_{i}"):
                        st.session_state[f"modifica_{i}"] = True
                    if st.session_state.get(f"modifica_{i}", False):
                        nuovo_inizio = st.date_input("Nuova data inizio", value=datetime.strptime(inizio, '%Y-%m-%d'), key=f"inizio_{i}")
                        nuovo_fine = st.date_input("Nuova data fine", value=datetime.strptime(fine, '%Y-%m-%d'), key=f"fine_{i}")
                        if st.button("Salva modifiche", key=f"save_{i}"):
                            if nuovo_inizio <= nuovo_fine:
                                data["disponibilita"][utente_corrente][i] = (nuovo_inizio.strftime('%Y-%m-%d'), nuovo_fine.strftime('%Y-%m-%d'))
                                data_manager.save_data(data)
                                st.session_state.data = data
                                st.session_state[f"modifica_{i}"] = False
                                st.success("✅ Modifica salvata!")
                            else:
                                st.error("❌ La data di inizio deve essere precedente alla data di fine!")
                with col_del:
                    if st.button("Elimina", key=f"del_{i}"):
                        data["disponibilita"][utente_corrente].pop(i)
                        if not data["disponibilita"][utente_corrente]:
                            del data["disponibilita"][utente_corrente]
                        data_manager.save_data(data)
                        st.session_state.data = data
                        st.success("🗑️ Periodo eliminato!")
                        st.rerun()
    else:
        st.info("Non hai ancora inserito disponibilità.")

    # Pulsante per resettare tutte le disponibilità personali
    if utente_corrente in data["disponibilita"] and data["disponibilita"][utente_corrente]:
        if st.button("🧹 Reset tutte le mie disponibilità"):
            del data["disponibilita"][utente_corrente]
            data_manager.save_data(data)
            st.session_state.data = data
            st.success("✅ Tutte le tue disponibilità sono state rimosse!")
            st.rerun()

    # Funzione per creare il calendario (invariata)
    def crea_calendario(disponibilita):
        date_list = []
        utenti_list = []
        colori_list = []
        
        for utente, periodi in disponibilita.items():
            colore = colori[utenti_registrati.index(utente) % len(colori)]
            for inizio, fine in periodi:
                inizio = datetime.strptime(inizio, '%Y-%m-%d')
                fine = datetime.strptime(fine, '%Y-%m-%d')
                delta = fine - inizio
                for i in range(delta.days + 1):
                    giorno = inizio + timedelta(days=i)
                    date_list.append(giorno)
                    utenti_list.append(utente)
                    colori_list.append(colore)
        
        df = pd.DataFrame({
            'Data': date_list,
            'Utente': utenti_list,
            'Colore': colori_list
        })
        return df

    # Visualizzazione del calendario
    st.subheader("📅 Disponibilità di tutti")
    if data["disponibilita"]:
        df_calendario = crea_calendario(data["disponibilita"])
        
        fig = px.scatter(
            df_calendario,
            x='Data',
            y='Utente',
            color='Utente',
            color_discrete_sequence=colori,
            title="Calendario Disponibilità di Gruppo"
        )
        fig.update_traces(marker=dict(size=12, opacity=0.8))
        fig.update_layout(
            height=500,  # Altezza aumentata
            showlegend=True,
            xaxis_title="Date",
            yaxis_title="Utenti",
            title_x=0.5,  # Centra il titolo
            margin=dict(l=50, r=50, t=50, b=50)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Scarica i dati del calendario
        csv = df_calendario.to_csv(index=False)
        st.download_button("📥 Scarica calendario", csv, "calendario_disponibilita.csv", "text/csv")

        # Trova settimane coincidenti
        def trova_settimane_comuni(disponibilita):
            date_per_utente = {}
            for utente, periodi in disponibilita.items():
                date_set = set()
                for inizio, fine in periodi:
                    inizio = datetime.strptime(inizio, '%Y-%m-%d')
                    fine = datetime.strptime(fine, '%Y-%m-%d')
                    delta = fine - inizio
                    for i in range(delta.days + 1):
                        date_set.add(inizio + timedelta(days=i))
                date_per_utente[utente] = date_set
            
            date_comuni = set.intersection(*date_per_utente.values())
            if not date_comuni:
                return None
                
            settimane_comuni = {}
            for data in sorted(date_comuni):
                numero_settimana = data.isocalendar()[1]
                anno = data.year
                chiave = f"Settimana {numero_settimana} ({anno})"
                if chiave not in settimane_comuni:
                    settimane_comuni[chiave] = []
                settimane_comuni[chiave].append(data)
                
            settimane_complete = {
                settimana: date 
                for settimana, date in settimane_comuni.items() 
                if len(date) >= 7
            }
            return settimane_complete

        st.subheader("🌟 Settimane consigliate per tutti")
        settimane_comuni = trova_settimane_comuni(data["disponibilita"])
        
        if settimane_comuni and len(settimane_comuni) > 0:
            for settimana, date in settimane_comuni.items():
                data_inizio = min(date)
                data_fine = max(date)
                st.markdown(f"**{settimana}**: dal {data_inizio.strftime('%d/%m/%Y')} al {data_fine.strftime('%d/%m/%Y')}")
        else:
            st.write("😕 Non ci sono settimane in cui tutti sono disponibili contemporaneamente.")
    else:
        st.info("Nessuna disponibilità inserita dal gruppo.")

if __name__ == "__main__":
    visualizza_calendario_disponibilita()