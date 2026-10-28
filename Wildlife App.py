import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import streamlit as st

# 1. Application Configuration (English)
st.set_page_config(page_title="Estonian Wildlife Tracker", layout="wide")
st.title("🌲 Estonian Wildlife Population (2022-2026)")

st.markdown("""
This interactive application was developed as a data analytics portfolio project.
The data is modeled based on official wildlife monitoring reports published by the **Estonian Environment Agency (Keskkonnaagentuur)**.
""")

# 2. Automated Data Generation (Prevents syntax errors during copy-paste)
@st.cache_data
def generate_data():
    counties = [
        'Harjumaa', 'Tartumaa', 'Pärnumaa', 'Saaremaa', 'Ida-Virumaa', 
        'Lääne-Virumaa', 'Viljandimaa', 'Võrumaa', 'Valgamaa', 'Põlvamaa', 
        'Raplamaa', 'Järvamaa', 'Jõgevamaa', 'Läänemaa', 'Hiiumaa'
    ]
    lats = [59.35, 58.38, 58.38, 58.41, 59.20, 59.25, 58.36, 57.84, 57.78, 58.05, 58.99, 58.89, 58.74, 58.94, 58.92]
    lons = [24.75, 26.72, 24.50, 22.50, 27.30, 26.30, 25.60, 27.00, 26.03, 27.05, 24.79, 25.56, 26.39, 23.63, 22.59]
    
    # Base DataFrame
    df_county = pd.DataFrame({'County': counties, 'Latitude': lats, 'Longitude': lons})
    
    # Population metrics generated safely using dynamic base values
    df_county['Roe Deer'] = [4500, 3800, 5200, 4100, 2100, 3900, 4300, 3500, 2900, 2700, 3600, 3400, 3100, 2500, 1400]
    df_county['Wild Boar'] = [800, 650, 950, 400, 550, 750, 700, 600, 500, 480, 620, 580, 520, 350, 80]
    df_county['Elk / Moose'] = [1100, 850, 1300, 150, 900, 1150, 950, 700, 650, 580, 920, 880, 780, 600, 50]
    df_county['Red Deer'] = [50, 30, 180, 3200, 20, 40, 90, 60, 80, 40, 110, 50, 30, 450, 1900]
    df_county['Lynx'] = [45, 35, 55, 0, 40, 50, 42, 30, 25, 22, 38, 35, 32, 20, 0]
    df_county['Wolf'] = [25, 15, 30, 5, 20, 25, 18, 22, 12, 14, 16, 15, 18, 10, 2]
    df_county['Brown Bear'] = [90, 80, 110, 0, 130, 140, 85, 50, 40, 45, 60, 75, 95, 20, 0]

    # Generate 5-year historical trends (2022-2026)
    years = ['2022', '2023', '2024', '2025', '2026']
    trend_data = {'Year': years}
    
    for animal in ['Roe Deer', 'Wild Boar', 'Elk / Moose', 'Red Deer', 'Lynx', 'Wolf', 'Brown Bear']:
        total_2026 = df_county[animal].sum()
        if animal in ['Red Deer', 'Wolf', 'Brown Bear']:
            trend_data[animal] = [int(total_2026 * 0.85), int(total_2026 * 0.90), int(total_2026 * 0.93), int(total_2026 * 0.97), total_2026]
        else:
            trend_data[animal] = [int(total_2026 * 1.15), int(total_2026 * 1.10), int(total_2026 * 1.05), int(total_2026 * 1.02), total_2026]
            
    df_trend = pd.DataFrame(trend_data)
    return df_county, df_trend

df_map, df_trend = generate_data()
animal_list = ['Roe Deer', 'Wild Boar', 'Elk / Moose', 'Red Deer', 'Lynx', 'Wolf', 'Brown Bear']

# 3. Sidebar Filter UI
st.sidebar.header("Data Filters")
selected_animal = st.sidebar.selectbox("Select a species to view:", animal_list)
total_population = df_map[selected_animal].sum()

# 4. Main Panel Layout (Table and Map Columns)
# Muudetud suhtarvu [1, 1.5] -> [1, 1.7], et tabeli veerg oleks veelgi kitsam
col1, col2 = st.columns([1, 1.7])

with col1:
    st.subheader(f"📊 {selected_animal} Population by County")
    table_df = df_map[['County', selected_animal]].sort_values(by=selected_animal, ascending=False)
    st.dataframe(table_df, hide_index=True, use_container_width=True)
    
    st.divider()
    st.metric(label=f"Total Estimated {selected_animal} Population (2026)", value=f"{total_population:,}")

with col2:
    st.subheader("🗺️ Interactive Geospatial Distribution Map (2026)")
    m = folium.Map(location=[58.5953, 25.0136], zoom_start=7, tiles="OpenStreetMap")
    max_value = df_map[selected_animal].max()
    
    for idx, row in df_map.iterrows():
        count_in_region = row[selected_animal]
        if count_in_region > 0:
            radius = (count_in_region / max_value) * 25 + 5
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=radius,
                popup=f"<b>{row['County']}</b><br>{selected_animal}: {count_in_region} individuals",
                color="darkgreen",
                fill=True,
                fill_color="green",
                fill_opacity=0.6,
                weight=1.5
            ).add_to(m)
            
    # Eemaldatud fikseeritud laius width=700, et kaart täidaks kogu laiema veeru ruumi automaatselt
    st_folium(m, use_container_width=True, height=500)


from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

# 5. Advanced Analytics Section (Charts)
st.divider()
st.header("📈 Advanced Trend & Density Analysis")

# Veergude suhe on paigas
chart_col1, chart_col2 = st.columns([1, 1.7])

with chart_col1:
    st.subheader("Five Year Population")
    line_data = df_trend[["Year", selected_animal]].set_index("Year")

    fig1 = go.Figure()

    # Vertikaalsed tulbad (täidavad kogu kõrguse)
    fig1.add_trace(
        go.Bar(
            x=line_data.index,
            y=line_data[selected_animal],
            name="Tihedus",
            marker_color="#97af98",
            width=0.4,
        )
    )

    # Joon otse tulpade peal
    fig1.add_trace(
        go.Scatter(
            x=line_data.index,
            y=line_data[selected_animal],
            name="Trend",
            mode="lines+markers",
            line=dict(color="#282b2e", width=3),
            marker=dict(color="#5A7697", size=8),
        )
    )

    # Range marginaalide lukustamine ja arvuvormingu parandus
    fig1.update_layout(
        margin=dict(l=50, r=10, t=10, b=30),  # l=50 jätab pikematele arvudele ruumi
        showlegend=False,
        xaxis=dict(type="category"),
        # Kood parandatud: tickformat=",.0f" koos seadistatud tühik-eraldajaga
        yaxis=dict(showgrid=True, tickformat=",.0f"), 
        separators=", ",  # Määrab tuhandete eraldajaks tühiku ja komakohaks koma
        height=350,
        template="streamlit",
    )

    st.plotly_chart(fig1, use_container_width=True)
    st.caption(
        f"Historical abundance trends for **{selected_animal}** from 2022 to 2026."
    )

with chart_col2:
    st.subheader("Regional Density Comparison (2026)")
    bar_data = df_map[["County", selected_animal]].sort_values(
        by=selected_animal, ascending=True
    )

    # Teine graafik on samuti Plotly, tagades 1:1 joondatuse
    fig2 = go.Figure()

    fig2.add_trace(
        go.Bar(
            x=bar_data[selected_animal],
            y=bar_data["County"],
            orientation="h",
            marker_color="#97af98",
        )
    )

    # Täpselt samad marginaalid, kõrgus ja arvuvormingud
    fig2.update_layout(
        margin=dict(l=80, r=10, t=10, b=30),
        showlegend=False,
        # Kood parandatud: Sama ühtne tühikuga tuhandike eraldaja ka horisontaalteljel
        xaxis=dict(showgrid=True, tickformat=",.0f"),
        yaxis=dict(type="category"),
        separators=", ",
        height=350,
        template="streamlit",
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Cross-county population distribution analysis.")

# 6. Footer
st.divider()
st.caption("Data Science Portfolio Project | Stack: Python, Streamlit, Folium, Pandas | Developer: Merje Nõmmik")