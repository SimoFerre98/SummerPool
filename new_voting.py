import streamlit as st
from data_manager import save_data

def visualizza_nuova_votazione():
    st.write(f"Benvenuto/a, {st.session_state.username}!")
    st.info(
        "**Come funziona la nuova votazione:** Seleziona fino a 2 destinazioni. "
        "Ogni destinazione scelta conta come un voto."
    )

    st.header("🆕 Nuova Votazione: Scegli fino a 2 destinazioni")
    nuove_destinazioni = ["Ibiza-Formentera", "Albania", "Sicilia", "Mykonos", "Portogallo", "Andalucia"]
    
    # Inizializza la chiave "nuovi_voti" se non esiste
    if "nuovi_voti" not in st.session_state.data:
        st.session_state.data["nuovi_voti"] = {}
    nuovi_voti_precedenti = st.session_state.data["nuovi_voti"].get(st.session_state.username, [])

    # Inizializza lo stato per le destinazioni selezionate
    if "nuove_destinazioni_selezionate" not in st.session_state:
        st.session_state.nuove_destinazioni_selezionate = []

    colonne_nuove = st.columns(3)
    for indice, destinazione in enumerate(nuove_destinazioni):
        with colonne_nuove[indice % 3]:
            default_value = destinazione in nuovi_voti_precedenti
            checkbox_key = f"nuova_dest_{indice}_{destinazione}"
            if st.checkbox(destinazione, key=checkbox_key, value=default_value):
                if destinazione not in st.session_state.nuove_destinazioni_selezionate:
                    st.session_state.nuove_destinazioni_selezionate.append(destinazione)
            else:
                if destinazione in st.session_state.nuove_destinazioni_selezionate:
                    st.session_state.nuove_destinazioni_selezionate.remove(destinazione)

    # Controlla se l'utente ha selezionato più di 2 destinazioni
    if len(st.session_state.nuove_destinazioni_selezionate) > 2:
        st.warning("Attenzione: puoi selezionare solo 2 destinazioni. Verranno considerate solo le prime 2 selezionate.")

    # Limita a 2 destinazioni
    nuove_selezionate = st.session_state.nuove_destinazioni_selezionate[:2]

    if nuove_selezionate:
        st.write("Destinazioni selezionate:")
        for dest in nuove_selezionate:
            st.write(f"- {dest}")

    # Pulsante per confermare i voti
    if st.button("Conferma Nuova Votazione"):
        if nuove_selezionate:
            st.session_state.data["nuovi_voti"][st.session_state.username] = nuove_selezionate
            save_data(st.session_state.data)
            st.success("Nuovi voti registrati con successo!")
        else:
            st.warning("Seleziona almeno una destinazione per la nuova votazione.")

    # Pulsante per resettare i voti
    if st.button("🔄 Resetta i tuoi voti"):
        # Cancella le selezioni correnti
        st.session_state.nuove_destinazioni_selezionate = []
        # Rimuovi i voti dell'utente dai dati salvati
        if st.session_state.username in st.session_state.data["nuovi_voti"]:
            del st.session_state.data["nuovi_voti"][st.session_state.username]
            save_data(st.session_state.data)
        st.success("I tuoi voti sono stati resettati con successo!")
        st.rerun()  # Ricarica la pagina per aggiornare le checkbox