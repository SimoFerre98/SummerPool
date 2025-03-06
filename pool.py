import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import account
import config
import auth
import voting
import details
import results
import data_manager
import calendar_disponibilita
import new_voting

# Inizializzazione dello stato
if 'utente_registrato' not in st.session_state:
    st.session_state.utente_registrato = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'azione_iniziale_selezionata' not in st.session_state:
    st.session_state.azione_iniziale_selezionata = False
if 'data' not in st.session_state:
    st.session_state.data = data_manager.load_data()
if 'utenti' not in st.session_state:
    st.session_state.utenti = st.session_state.data.get("utenti", {})
if 'voti_totali' not in st.session_state:
    st.session_state.voti_totali = {}
if 'voti_utente' not in st.session_state:
    st.session_state.voti_utente = None
if 'tutti_i_voti' not in st.session_state:
    st.session_state.tutti_i_voti = st.session_state.data.get("voti", {})
if 'destinazioni_selezionate_ordine' not in st.session_state:
    st.session_state.destinazioni_selezionate_ordine = []
if 'nuove_destinazioni_selezionate' not in st.session_state:
    st.session_state.nuove_destinazioni_selezionate = []

# Sidebar con pulsanti
with st.sidebar:
    st.image("logo.png", width=100)
    st.markdown("### Menu di Navigazione")

    sezioni = {
        "🗳️ Pool di Votazione": "Pool di Votazione",
        "🆕 Nuova Votazione": "Nuova Votazione",
        "ℹ️ Dettagli Destinazioni": "Dettagli Destinazioni",
        "📊 Risultati": "Risultati",
        "🗓️ Disponibilità Calendario": "Disponibilità Calendario",
        "⚙️ Impostazioni": "Impostazioni"
    }

    for label, valore in sezioni.items():
        if st.button(label, key=valore):
            st.session_state.sezione_selezionata = valore

    if st.session_state.utente_registrato:
        if st.button("🚪 Logout"):
            st.session_state.utente_registrato = False
            st.session_state.username = ''
            st.session_state.azione_iniziale_selezionata = False
            st.session_state.destinazioni_selezionate_ordine = []
            st.session_state.nuove_destinazioni_selezionate = []
            st.session_state.voti_utente = None
            st.success("Logout effettuato con successo.")
            st.rerun()

# Titolo principale
st.title("Sondaggio Destinazioni Vacanze")

# Testo introduttivo condizionale
sezione_selezionata = st.session_state.get("sezione_selezionata", "Pool di Votazione")
if sezione_selezionata == "Pool di Votazione":
    st.markdown(
        """
        **Benvenuto al Sondaggio!** 👋
        Per navigare tra le sezioni, utilizza i pulsanti nel pannello laterale a sinistra.
        _(Se il pannello laterale è chiuso, clicca sull'icona ☰ in alto a sinistra per aprirlo)._
        """
    )
elif sezione_selezionata == "Nuova Votazione":
    st.markdown(
        """
        **Nuova Votazione!** 🆕
        Qui puoi votare fino a 2 destinazioni tra quelle selezionate per la nuova tornata.
        """
    )
elif sezione_selezionata == "Disponibilità Calendario":
    st.markdown(
        """
        **Calendario Disponibilità Vacanze** 🗓️
        In questa sezione puoi **segnalare i tuoi periodi di disponibilità** per le vacanze.
        Seleziona le date sul calendario per indicare quando sei disponibile.
        """
    )
elif sezione_selezionata == "Impostazioni":
    st.markdown(
        """
        **Impostazioni Profilo** ⚙️
        Gestisci il tuo account e la tua password qui.
        """
    )

# Logica delle sezioni
if sezione_selezionata == "Pool di Votazione":
    if not st.session_state.utente_registrato:
        auth.gestisci_avviso_privacy_password()
        azione = st.radio("Seleziona l'azione:", ["Login", "Registrazione"])
        if azione == "Registrazione":
            auth.gestisci_registrazione()
        elif azione == "Login":
            auth.gestisci_login()
    else:
        voting.visualizza_pool_votazione(config.DESTINAZIONI)
elif sezione_selezionata == "Nuova Votazione":
    if not st.session_state.utente_registrato:
        auth.gestisci_avviso_privacy_password()
        azione = st.radio("Seleziona l'azione:", ["Login", "Registrazione"])
        if azione == "Registrazione":
            auth.gestisci_registrazione()
        elif azione == "Login":
            auth.gestisci_login()
    else:
        new_voting.visualizza_nuova_votazione()
elif sezione_selezionata == "Dettagli Destinazioni":
    details.visualizza_dettagli_destinazioni(config.DESTINAZIONI)
elif sezione_selezionata == "Risultati":
    results.visualizza_risultati_protetti()
elif sezione_selezionata == "Disponibilità Calendario":
    calendar_disponibilita.visualizza_calendario_disponibilita()
elif sezione_selezionata == "Impostazioni":
    if st.session_state.utente_registrato:
        st.subheader(f"Gestione profilo di {st.session_state.username}")
        account.gestisci_cambio_password()
        if st.session_state.username == "ferre":
            st.subheader("Backup Database")
            if st.button("📥 Scarica database"):
                with open("database.json", "r") as f:
                    json_data = f.read()
                st.download_button("Scarica JSON", json_data, "database.json", "application/json")

            # Gestione visibilità risultati nuova votazione
            st.subheader("Gestione Visibilità Risultati Nuova Votazione")
            if "utenti_autorizzati_nuovi_voti" not in st.session_state.data:
                st.session_state.data["utenti_autorizzati_nuovi_voti"] = ["ferre"]  # Default: solo admin
            utenti_registrati = list(st.session_state.data["utenti"].keys())
            utenti_autorizzati = st.multiselect(
                "Seleziona chi può vedere i risultati della nuova votazione:",
                options=utenti_registrati,
                default=st.session_state.data["utenti_autorizzati_nuovi_voti"]
            )
            if utenti_autorizzati != st.session_state.data["utenti_autorizzati_nuovi_voti"]:
                st.session_state.data["utenti_autorizzati_nuovi_voti"] = utenti_autorizzati
                data_manager.save_data(st.session_state.data)
                st.success("Lista degli utenti autorizzati aggiornata!")
    else:
        st.warning("🚫 Devi essere loggato per accedere alle impostazioni!")