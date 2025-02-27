import streamlit as st
import pandas as pd

# Dizionario delle coordinate
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

def visualizza_dettagli_destinazioni(destinazioni):
    st.subheader("🌍 Mappa delle Destinazioni")
    
    # Creazione del DataFrame per la mappa
    lat_list = []
    lon_list = []
    nome_list = []

    for d in destinazioni:
        coords = coordinate_destinazioni.get(d)
        if coords is not None:
            lat_list.append(coords[0])
            lon_list.append(coords[1])
            nome_list.append(d)

    df = pd.DataFrame({
        'lat': lat_list,
        'lon': lon_list,
        'dest': nome_list
    })

    if not df.empty:
        st.map(df, zoom=2, use_container_width=True)
    else:
        st.write("Mappa non disponibile (nessuna coordinata definita).")

    # Link a Notion
    st.markdown("📖 Per maggiori informazioni sulle destinazioni, consulta la nostra pagina Notion:")
    st.markdown("[Vai a Notion](https://ferremede.notion.site/Vacanza-2k25-1a24febbe94a80f2900cfb614e5939f9?pvs=4)")  # Sostituisci con il tuo link reale

if __name__ == "__main__":
    st.title("Test Mappa")
    lista = list(coordinate_destinazioni.keys())
    visualizza_dettagli_destinazioni(lista)