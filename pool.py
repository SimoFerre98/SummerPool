import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

DATABASE_FILE = "database.json"

# Ordina le destinazioni alfabeticamente
destinazioni = [
    "Albania", "Alicante/Benidorm", "Amsterdam/Copenhagen", "Andalucia", "Baku", "Bangkock", "Corsica",
    "Cipro", "Egitto", "Ibiza-Formentera", "Islanda", "Isole Faroe", "Istanbul", "Kos", "Malta",
    "Marocco", "Montenegro", "Mykonos", "Portogallo", "Puglia", "Sicilia"
]
destinazioni.sort() # Ordina la lista in-place

# *** DEFINIZIONE DIZIONARI COORDINATE E IMMAGINI - SPOSTATI IN SCOPO GLOBALE ***
coordinate_destinazioni = { # Dizionario: "Nome Destinazione": (latitudine, longitudine)
    "Albania": (41.3275, 19.8187),        # Tirana, Albania (esempio)
    "Alicante/Benidorm": (38.5417, -0.1211), # Alicante, Spagna (esempio)
    "Amsterdam/Copenhagen": (52.3676, 4.9041), # Amsterdam, Paesi Bassi (esempio)
    "Andalucia": (37.6293, -4.7703),      # Cordoba, Andalucia (esempio)
    "Baku": (40.3777, 49.8920),           # Baku, Azerbaijan (esempio)
    "Bangkock": (13.7563, 100.5018),       # Bangkok, Thailandia (esempio)
    "Corsica": (42.0930, 9.1276),         # Ajaccio, Corsica (esempio)
    "Cipro": (35.1264, 33.4299),          # Nicosia, Cipro (esempio)
    "Egitto": (26.8206, 30.8025),         # Cairo, Egitto (esempio)
    "Ibiza-Formentera": (39.0200, 1.4813),   # Ibiza, Spagna (esempio)
    "Islanda": (64.1466, -21.9426),        # Reykjavik, Islanda (esempio)
    "Isole Faroe": (62.0152, -6.7704),     # Torshavn, Isole Faroe (esempio)
    "Istanbul": (41.0082, 28.9784),        # Istanbul, Turchia (esempio)
    "Kos": (36.9042, 27.2976),            # Kos, Grecia (esempio)
    "Malta": (35.9375, 14.5001),           # Valletta, Malta (esempio)
    "Marocco": (31.7917, -7.0926),        # Rabat, Marocco (esempio)
    "Montenegro": (42.4431, 19.2645),      # Podgorica, Montenegro (esempio)
    "Mykonos": (37.4457, 25.3273),         # Mykonos, Grecia (esempio)
    "Portogallo": (38.7223, -9.1393),      # Lisbona, Portogallo (esempio)
    "Puglia": (41.1256, 16.8639),         # Bari, Puglia (esempio)
    "Sicilia": (38.1156, 13.3613),         # Palermo, Sicilia (esempio)
}

url_immagini_destinazioni = { # Dizionario: "Nome Destinazione": "URL Immagine Online"
    "Albania": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/ALB_location_map.svg/400px-ALB_location_map.svg.png", # Mappa Albania (esempio)
    "Alicante/Benidorm": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Benidorm_Levante_beach_and_skyline.jpg/800px-Benidorm_Levante_beach_and_skyline.jpg", # Benidorm (esempio)
    "Amsterdam/Copenhagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Nyhavn_Copenhagen_Denmark.jpg/800px-Nyhavn_Copenhagen_Denmark.jpg", # Copenhagen (esempio)
    "Andalucia": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Andalusia_in_Spain_%28location_map%29.svg/400px-Andalusia_in_Spain_%28location_map%29.svg.png", # Andalusia (esempio)
    "Baku": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Baku_Flame_Towers_and_skyline_at_night.jpg/800px-Baku_Flame_Towers_and_skyline_at_night.jpg", # Baku (esempio)
    "Bangkock": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Temple_of_Dawn_Bangkok_Thailand.jpg/800px-Temple_of_Dawn_Bangkok_Thailand.jpg", # Bangkok (esempio)
    "Corsica": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Corse-topo.svg/450px-Corse-topo.svg.png", # Mappa Corsica (esempio)
    "Cipro": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Cyprus_%28location_map%29.svg/500px-Cyprus_%28location_map%29.svg.png", # Mappa Cipro (esempio)
    "Egitto": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Egypt_location_map.svg/500px-Egypt_location_map.svg.png", # Mappa Egitto (esempio)
    "Ibiza-Formentera": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Location_map_Ibiza.png/400px-Location_map_Ibiza.png", # Mappa Ibiza (esempio)
    "Islanda": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Iceland_location_map.svg/500px-Iceland_location_map.svg.png", # Mappa Islanda (esempio)
    "Isole Faroe": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Location_Faroes.png/400px-Location_Faroes.png", # Mappa Isole Faroe (esempio)
    "Istanbul": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Turkey_location_map_Istanbul.svg/500px-Turkey_location_map_Istanbul.svg.png", # Mappa Istanbul (esempio)
    "Kos": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Greece_location_map_Kos.svg/400px-Greece_location_map_Kos.svg.png", # Mappa Kos (esempio)
    "Malta": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Malta_location_map.svg/500px-Malta_location_map.svg.png", # Mappa Malta (esempio)
    "Marocco": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Morocco_location_map.svg/500px-Morocco_location_map.svg.png", # Mappa Marocco (esempio)
    "Montenegro": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Montenegro_location_map.svg/450px-Montenegro_location_map.svg.png", # Mappa Montenegro (esempio)
    "Mykonos": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Cyclades_location_map_Mykonos.svg/400px-Cyclades_location_map_Mykonos.svg.png", # Mappa Mykonos (esempio)
    "Portogallo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Portugal_location_map.svg/500px-Portugal_location_map.svg.png", # Mappa Portogallo (esempio)
    "Puglia": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Puglia_in_Italy.svg/500px-Puglia_in_Italy.svg.png", # Mappa Puglia (esempio)
    "Sicilia": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Sicilia_in_Italy.svg/500px-Sicilia_in_Italy.svg.png", # Mappa Sicilia (esempio)
}
# *** FINE DEFINIZIONE DIZIONARI COORDINATE E IMMAGINI ***


def load_data():
    try:
        with open(DATABASE_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"utenti": {}, "voti": {}}
    return data

def save_data(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'utente_registrato' not in st.session_state:
    st.session_state.utente_registrato = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'azione_iniziale_selezionata' not in st.session_state:
    st.session_state.azione_iniziale_selezionata = False
if 'data' not in st.session_state:
    st.session_state.data = load_data()
if 'utenti' not in st.session_state:
    st.session_state.utenti = st.session_state.data.get("utenti", {})
if 'voti_totali' not in st.session_state:
    st.session_state.voti_totali = {}
if 'voti_utente' not in st.session_state:
    st.session_state.voti_utente = None
if 'tutti_i_voti' not in st.session_state:
    st.session_state.tutti_i_voti = st.session_state.data.get("voti", {})
if 'destinazioni_selezionate_ordine' not in st.session_state:
    st.session_state.destinazioni_selezionate_ordine = [] # Inizializzazione lista ordinata

# *** INIZIO BLOCCO CODICE INSERITO: MENU LATERALE ***
with st.sidebar:
    st.image("logo.png", width=100) # Logo nel sidebar (opzionale)
    sezione_selezionata = st.selectbox(
        "Menu di Navigazione",
        ["Pool di Votazione", "Dettagli Destinazioni"] # Voci del menu
    )
# *** FINE BLOCCO CODICE INSERITO: MENU LATERALE ***

# Titolo principale (fuori dal sidebar)
st.title("Sondaggio Destinazioni Vacanze")

# *** INIZIO BLOCCO CODICE INSERITO: SEZIONE "POOL DI VOTAZIONE" ***
if sezione_selezionata == "Pool di Votazione": # Mostra il codice di votazione SOLO se selezionato nel menu

    if not st.session_state.utente_registrato:
        # **INIZIO BLOCCO CODICE INSERITO: AVVISO PRIVACY PASSWORD**
        st.warning(
            "**Avviso Importante sulla Privacy:** Le password inserite per la registrazione "
            "non sono criptate e vengono memorizzate in chiaro. "
            "Si raccomanda vivamente di **non utilizzare password personali o sensibili** "
            "che usi per altri servizi importanti. "
            "Il creatore di questo sito ha la possibilità tecnica di visualizzare le password inserite."
        )
        # **FINE BLOCCO CODICE INSERITO: AVVISO PRIVACY PASSWORD**

        azione = st.radio("Seleziona l'azione:", ["Login", "Registrazione"])

        if azione == "Registrazione":
            nuovo_username = st.text_input("Username per la registrazione").lower()
            nuova_password = st.text_input("Password per la registrazione", type="password")
            if st.button("Registrati"):
                if nuovo_username in st.session_state.utenti:
                    st.error("Username già esistente. Scegli un altro username.")
                else:
                    st.session_state.utenti[nuovo_username] = nuova_password
                    st.session_state.data["utenti"][nuovo_username] = nuova_password
                    st.session_state.data["voti"][nuovo_username] = {}
                    save_data(st.session_state.data)
                    st.success("Registrazione completata con successo! Effettua il login.")
                    # **INIZIO LINEE CODICE INSERITE: LOGIN AUTOMATICO DOPO REGISTRAZIONE**
                    st.session_state.utente_registrato = True
                    st.session_state.username = nuovo_username
                    # **FINE LINEE CODICE INSERITE: LOGIN AUTOMATICO DOPO REGISTRAZIONE**
                    st.session_state.azione_iniziale_selezionata = True
                    st.rerun()
        elif azione == "Login":
            username_login = st.text_input("Username per il login").lower()
            password_login = st.text_input("Password per il login", type="password")
            # **INIZIO LINEA CODICE INSERITA: AVVISO PASSWORD DIMENTICATA**
            st.caption("In caso di password dimenticata, contatta l'amministratore del sito.")
            # **FINE LINEA CODICE INSERITA: AVVISO PASSWORD DIMENTICATA**
            if st.button("Login"):
                if username_login in st.session_state.utenti and st.session_state.utenti[username_login] == password_login:
                    st.session_state.utente_registrato = True
                    st.session_state.username = username_login
                    st.success(f"Login effettuato con successo, benvenuto {username_login}!")
                    st.session_state.azione_iniziale_selezionata = True
                    st.rerun()
                else:
                    st.error("Credenziali non valide. Riprova.")
    else:
        st.write(f"Benvenuto, {st.session_state.username}!")
        # **INIZIO BLOCCO CODICE INSERITO: ISTRUZIONI VOTAZIONE**
        st.info(
            "**Come funziona la votazione:** Seleziona fino a 4 destinazioni che preferisci. "
            "La **prima destinazione** che selezioni riceverà **4 punti**, la **seconda 3 punti**, "
            "la **terza 2 punti** e la **quarta 1 punto**. "
            "Se selezioni più di 4 destinazioni, verranno considerate solo le prime 4 in ordine di selezione."
        )
        # **FINE BLOCCO CODICE INSERITO: ISTRUZIONI VOTAZIONE**

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

# *** FINE BLOCCO CODICE INSERITO: SEZIONE "POOL DI VOTAZIONE" ***

# *** INIZIO BLOCCO CODICE MODIFICATO: SEZIONE "DETTAGLI DESTINAZIONI" - SINGOLA MAPPA ***
elif sezione_selezionata == "Dettagli Destinazioni":  # Mostra questa sezione se "Dettagli Destinazioni" è selezionato

    st.header("Mappa Interattiva delle Destinazioni")  # Intestazione per la mappa

    st.write("Visualizza le posizioni di tutte le destinazioni sulla mappa:")  # Testo introduttivo mappa

    # *** PREPARAZIONE DATI PER LA MAPPA UNICA ***
    lista_latitudini = []
    lista_longitudini = []
    lista_nomi_destinazioni_mappa = []  # Per etichette (opzionale, se vuoi nomi sui segnaposto)

    for destinazione in destinazioni:
        coordinate = coordinate_destinazioni.get(destinazione)
        if coordinate:
            latitudine, longitudine = coordinate
            lista_latitudini.append(latitudine)
            lista_longitudini.append(longitudine)
            lista_nomi_destinazioni_mappa.append(destinazione) # Aggiungi nome per etichetta (opzionale)

    # Crea DataFrame per la mappa UNICA con tutte le destinazioni
    data_mappa_totale = pd.DataFrame({
        'latitude': lista_latitudini,
        'longitude': lista_longitudini,
        'destinazione': lista_nomi_destinazioni_mappa # Colonna opzionale per etichette
    })

    # *** MODIFICA: RINOMINA COLONNE DATAFRAME PER COMPATIBILITÀ st.map() ***
    data_mappa_totale = data_mappa_totale.rename(columns={'latitude': 'lat', 'longitude': 'lon'})


    # *** MAPPA UNICA CON SEGNAPOSTO PER TUTTE LE DESTINAZIONI ***
    if not data_mappa_totale.empty: # Mostra la mappa solo se ci sono dati
        st.map(data_mappa_totale,
               zoom=2) # Zoom iniziale per vedere tutte le destinazioni globalmente (regola zoom se necessario)
    else:
        st.write("Mappa non disponibile (nessuna coordinata definita).")


    st.header("Dettagli e Immagini delle Destinazioni") # Intestazione per le immagini (sotto la mappa)
    st.write("Esplora le immagini di ogni destinazione:") # Testo introduttivo immagini

    colonne_destinazioni = st.columns(3) # Crea 3 colonne per layout immagini

    for indice, destinazione in enumerate(destinazioni):
        with colonne_destinazioni[indice % 3]: # Distribuisci in 3 colonne
            st.subheader(destinazione) # Sottotitolo con nome destinazione

            # *** IMMAGINE DA URL ONLINE ***
            url_immagine = url_immagini_destinazioni.get(destinazione) # Ottieni URL immagine dal dizionario
            if url_immagine:
                st.image(url_immagine, width=200) # Mostra immagine da URL
            else:
                st.write("Immagine non disponibile") # Se non c'è URL, mostra messaggio

# *** FINE BLOCCO CODICE MODIFICATO: SEZIONE "DETTAGLI DESTINAZIONI" - SINGOLA MAPPA ***