import streamlit as st
import pandas as pd

# --- DIZIONARIO COORDINATE ---
coordinate_destinazioni = {
    "Albania": (41.3275, 19.8187),           # Tirana
    "Alicante/Benidorm": (38.5417, -0.1211), # Alicante
    "Amsterdam/Copenhagen": (52.3676, 4.9041), # Amsterdam
    "Andalucia": (37.6293, -4.7703),         # Cordoba
    "Baku": (40.3777, 49.8920),              # Baku, Azerbaijan
    "Bangkok": (13.7563, 100.5018),          # Bangkok, Thailandia
    "Corsica": (42.0930, 9.1276),            # Ajaccio
    "Cipro": (35.1264, 33.4299),             # Nicosia
    "Egitto": (26.8206, 30.8025),            # Cairo (appross.)
    "Ibiza-Formentera": (39.0200, 1.4813),   # Ibiza
    "Islanda": (64.1466, -21.9426),          # Reykjavik
    "Isole Faroe": (62.0152, -6.7704),       # Torshavn
    "Istanbul": (41.0082, 28.9784),          # Istanbul, Turchia
    "Kos": (36.9042, 27.2976),               # Kos, Grecia
    "Malta": (35.9375, 14.5001),             # Valletta
    "Marocco": (31.7917, -7.0926),           # Rabat (appross.)
    "Montenegro": (42.4431, 19.2645),        # Podgorica
    "Mykonos": (37.4457, 25.3273),           # Mykonos, Grecia
    "Portogallo": (38.7223, -9.1393),        # Lisbona
    "Puglia": (41.1256, 16.8639),            # Bari
    "Sicilia": (38.1156, 13.3613),           # Palermo
}

# --- DIZIONARIO IMMAGINI (LINK DIRETTI WIKIPEDIA COMMONS) ---
url_immagini_destinazioni = {
    "Albania": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/ALB_location_map.svg/400px-ALB_location_map.svg.png",
    "Alicante/Benidorm": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Benidorm_Levante_beach_and_skyline.jpg/800px-Benidorm_Levante_beach_and_skyline.jpg",
    "Amsterdam/Copenhagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Nyhavn_Copenhagen_Denmark.jpg/800px-Nyhavn_Copenhagen_Denmark.jpg",
    "Andalucia": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Andalusia_in_Spain_%28location_map%29.svg/400px-Andalusia_in_Spain_%28location_map%29.svg.png",
    "Baku": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Baku_Flame_Towers_and_skyline_at_night.jpg/800px-Baku_Flame_Towers_and_skyline_at_night.jpg",
    "Bangkok": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Temple_of_Dawn_Bangkok_Thailand.jpg/800px-Temple_of_Dawn_Bangkok_Thailand.jpg",
    "Corsica": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Corse-topo.svg/450px-Corse-topo.svg.png",
    "Cipro": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Cyprus_%28location_map%29.svg/500px-Cyprus_%28location_map%29.svg.png",
    "Egitto": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Egypt_location_map.svg/500px-Egypt_location_map.svg.png",
    "Ibiza-Formentera": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Location_map_Ibiza.png/400px-Location_map_Ibiza.png",
    "Islanda": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Iceland_location_map.svg/500px-Iceland_location_map.svg.png",
    "Isole Faroe": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Location_Faroes.png/400px-Location_Faroes.png",
    "Istanbul": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Turkey_location_map_Istanbul.svg/500px-Turkey_location_map_Istanbul.svg.png",
    "Kos": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Greece_location_map_Kos.svg/400px-Greece_location_map_Kos.svg.png",
    "Malta": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Malta_location_map.svg/500px-Malta_location_map.svg.png",
    "Marocco": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Morocco_location_map.svg/500px-Morocco_location_map.svg.png",
    "Montenegro": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Montenegro_location_map.svg/450px-Montenegro_location_map.svg.png",
    "Mykonos": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Cyclades_location_map_Mykonos.svg/400px-Cyclades_location_map_Mykonos.svg.png",
    "Portogallo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Portugal_location_map.svg/500px-Portugal_location_map.svg.png",
    "Puglia": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Puglia_in_Italy.svg/500px-Puglia_in_Italy.svg.png",
    "Sicilia": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Sicilia_in_Italy.svg/500px-Sicilia_in_Italy.svg.png",
}

def visualizza_dettagli_destinazioni(destinazioni):
    st.header("Mappa Interattiva delle Destinazioni")
    st.write("Visualizza le posizioni di tutte le destinazioni sulla mappa:")

    # Liste per costruire il DataFrame per st.map()
    lat_list = []
    lon_list = []
    nome_list = []

    for d in destinazioni:
        coords = coordinate_destinazioni.get(d)
        if coords is not None:
            lat_list.append(coords[0])
            lon_list.append(coords[1])
            nome_list.append(d)

    # Creiamo il DataFrame per la mappa
    df = pd.DataFrame({
        'lat': lat_list,
        'lon': lon_list,
        'dest': nome_list
    })

    if not df.empty:
        st.map(df, zoom=2)
    else:
        st.write("Mappa non disponibile (nessuna coordinata definita).")

    st.header("Dettagli e Immagini delle Destinazioni")
    st.write("Esplora le immagini di ogni destinazione:")

    # Disposizione in 3 colonne
    col3 = st.columns(3)
    for i, d in enumerate(destinazioni):
        with col3[i % 3]:
            st.subheader(d)
            url_immagine = url_immagini_destinazioni.get(d)
            if url_immagine:
                st.image(url_immagine, width=200)
            else:
                st.write("Immagine non disponibile")

# --- ESEMPIO DI ESECUZIONE ---
if __name__ == "__main__":
    st.title("Test di Immagini da Wikipedia Commons")
    lista = list(coordinate_destinazioni.keys())
    visualizza_dettagli_destinazioni(lista)
