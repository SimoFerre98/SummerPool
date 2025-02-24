import streamlit as st
import pandas as pd

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

def visualizza_dettagli_destinazioni(destinazioni): # Riceve la lista delle destinazioni come argomento
    st.header("Mappa Interattiva delle Destinazioni")
    st.write("Visualizza le posizioni di tutte le destinazioni sulla mappa:")

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

    st.header("Dettagli e Immagini delle Destinazioni")
    st.write("Esplora le immagini di ogni destinazione:")

    colonne_destinazioni = st.columns(3)

    for indice, destinazione in enumerate(destinazioni):
        with colonne_destinazioni[indice % 3]:
            st.subheader(destinazione)

            # *** IMMAGINE DA URL ONLINE ***
            url_immagine = url_immagini_destinazioni.get(destinazione)
            if url_immagine:
                st.image(url_immagine, width=200)
            else:
                st.write("Immagine non disponibile")