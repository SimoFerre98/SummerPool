import streamlit as st
import pandas as pd
import plotly.express as px

# Coordinate delle destinazioni
coordinate_destinazioni = {
    "Albania": (41.3275, 19.8187),
    "Alicante/Benidorm": (38.5417, -0.1211),
    "Amsterdam/Copenhagen": (52.3676, 4.9041),
    "Andalucia": (37.6293, -4.7703),
    "Baku": (40.3777, 49.8920),
    "Bangkok": (13.7563, 100.5018),
    "Corsica": (42.0930, 9.1276),
    "Cipro": (35.1264, 33.4299),
    "Egitto": (26.8206, 30.8025),
    "Ibiza-Formentera": (39.0200, 1.4813),
    "Islanda": (64.1466, -21.9426),
    "Isole Faroe": (62.0152, -6.7704),
    "Istanbul": (41.0082, 28.9784),
    "Kos": (36.9042, 27.2976),
    "Malta": (35.9375, 14.5001),
    "Marocco": (31.7917, -7.0926),
    "Montenegro": (42.4431, 19.2645),
    "Mykonos": (37.4457, 25.3273),
    "Portogallo": (38.7223, -9.1393),
    "Puglia": (41.1256, 16.8639),
    "Sicilia": (38.1156, 13.3613),
}

def visualizza_mappa(destinazioni):
    st.subheader("🌍 Mappa delle Tue Destinazioni")

    # Creazione del DataFrame per la mappa
    lat_list = [coordinate_destinazioni[d][0] for d in destinazioni if d in coordinate_destinazioni]
    lon_list = [coordinate_destinazioni[d][1] for d in destinazioni if d in coordinate_destinazioni]
    nome_list = [d for d in destinazioni if d in coordinate_destinazioni]

    df = pd.DataFrame({
        'lat': lat_list,
        'lon': lon_list,
        'dest': nome_list
    })

    if not df.empty:
        # Creazione della mappa con marker personalizzati
        fig = px.scatter_geo(
            df,
            lat='lat',
            lon='lon',
            text='dest',
            hover_name='dest',
            size_max=15,
            projection="natural earth",
        )
        fig.update_traces(marker=dict(size=12, color="#FF6B6B", symbol="circle"))  # Colore rosso corallo per i marker
        fig.update_layout(
            geo=dict(
                showland=True,
                landcolor="rgb(243, 243, 243)",  # Colore chiaro per la terra
                countrycolor="rgb(204, 204, 204)",  # Bordi dei paesi
            ),
            height=500,
            margin={"r":0, "t":0, "l":0, "b":0}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Nessuna destinazione valida da mostrare sulla mappa.")

    # Aggiunta di un link opzionale
    st.markdown("📖 Vuoi più dettagli? Consulta la nostra pagina Notion: [Vai a Notion](https://www.notion.so/Esempio-Destinazioni-Vacanze)")

# Esecuzione
if __name__ == "__main__":
    st.title("Esplora i Tuoi Viaggi")
    st.write("Ecco una mappa interattiva con le destinazioni che ti piacerebbe visitare!")
    destinazioni = list(coordinate_destinazioni.keys())
    visualizza_mappa(destinazioni)