import streamlit as st
from data_manager import save_data # Importa la funzione per salvare i dati

def visualizza_pool_votazione(destinazioni): # Riceve la lista delle destinazioni come argomento
    st.write(f"Benvenuto/a, {st.session_state.username}!")
    st.info(
        "**Come funziona la votazione:** Seleziona fino a 4 destinazioni che preferisci. "
        "La **prima destinazione** che selezioni riceverà **4 punti**, la **seconda 3 punti**, "
        "la **terza 2 punti** e la **quarta 1 punto**. "
        "Se selezioni più di 4 destinazioni, verranno considerate solo le prime 4 in ordine di selezione."
    )

    st.header("Vota le tue 4 destinazioni preferite:")
    destinazioni_selezionate = [] # RIMOSSA - Usa st.session_state.destinazioni_selezionate_ordine
    punti_voto_assegnati = {}
    colonne = st.columns(4)
    punti_disponibili = [4, 3, 2, 1]

    # Carica i voti precedenti dell'utente, se esistono
    voti_precedenti = st.session_state.data["voti"].get(st.session_state.username, {})
    destinazioni_votate_precedentemente = list(voti_precedenti.keys())

    for indice, destinazione in enumerate(destinazioni):
        with colonne[indice % 4]:
            default_value = destinazione in destinazioni_votate_precedentemente
            checkbox_key = f"dest_{indice}_{destinazione}"
            checkbox_value = st.checkbox(destinazione, key=checkbox_key, value=default_value)

            if checkbox_value:
                # Se la checkbox è selezionata:
                if destinazione not in st.session_state.destinazioni_selezionate_ordine:
                    # Aggiungi alla lista ORDINATA SOLO se non è già presente
                    st.session_state.destinazioni_selezionate_ordine.append(destinazione)
            else:
                # Se la checkbox è DESELEZIONATA:
                if destinazione in st.session_state.destinazioni_selezionate_ordine:
                    # Rimuovi dalla lista ORDINATA se presente
                    st.session_state.destinazioni_selezionate_ordine.remove(destinazione)

    # Usa la lista ORDINATA da session_state per le operazioni successive
    destinazioni_selezionate = st.session_state.destinazioni_selezionate_ordine

    if len(destinazioni_selezionate) > 4:
        st.warning("Hai selezionato più di 4 destinazioni. Solo le prime 4 saranno considerate per il voto.")
        destinazioni_selezionate = destinazioni_selezionate[:4]

    # Assegna i punti ALLE DESTINAZIONI SELEZIONATE in base all'ordine DI SELEZIONE
    punti_voto_assegnati = {}
    for i, destinazione in enumerate(destinazioni_selezionate):
        if i < 4:
            punti_voto_assegnati[destinazione] = punti_disponibili[i]

    # RIPRISTINO visualizzazione elenco puntato sotto i checkbox:
    if destinazioni_selezionate:
        st.write("Destinazioni selezionate e punti:")
        for i, destinazione in enumerate(destinazioni_selezionate):
            punti = punti_voto_assegnati.get(destinazione, 0)
            st.write(f"- {destinazione} ({punti} punti)")

    if st.button("Conferma Voti"):
        if len(destinazioni_selezionate) > 0:
            st.session_state.voti_utente = destinazioni_selezionate

            voti_con_valore = punti_voto_assegnati

            st.session_state.data["voti"][st.session_state.username] = voti_con_valore
            save_data(st.session_state.data)
            st.success("Voti registrati con successo!")
            del st.session_state.voti_utente
        else:
            st.warning("Seleziona almeno una destinazione prima di confermare.")