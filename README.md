markdown
🚀 **[Click here to view the Live Demo]([PASTE_YOUR_STREAMLIT_URL_HERE](https://estonian-wildlife-population.streamlit.app))**
# 🌲 Estonian Wildlife Population

An interactive Streamlit web application designed to visualize and analyze wildlife population trends and regional density distributions in Estonia from 2022 to 2026. This project serves as a data analytics portfolio piece, utilizing modeled data inspired by official wildlife monitoring reports published by the **Estonian Environment Agency (Keskkonnaagentuur)**.

---

## ✨ Features

- **Dynamic Data Filtering:** Easily select from various Estonian wildlife species (Roe Deer, Wild Boar, Elk/Moose, Red Deer, Lynx, Wolf, Brown Bear) via a clean sidebar UI.
- **Geospatial Visualization:** Features an interactive map built with `folium` that displays relative population densities across Estonian counties using dynamic circle markers.
- **Advanced Trend Analysis:** Displays a custom-built, dual-axis Plotly chart combining 5-year historical trajectories (line chart) and population metrics (vertical bar charts) aligned side-by-side with horizontal density comparisons.
- **Clean Data Formatting:** All metrics and chart legends are formatted with unified spacing and native numerical formatting (e.g., thousands separators without confusing scientific shorthands like "K").

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Streamlit** (UI Framework)
- **Plotly** (Advanced Interactive Graphics)
- **Folium & Streamlit-Folium** (Geospatial Mapping)
- **Pandas** (Data Manipulation)

---

## 📦 Installation & Setup

Follow these steps to run the application locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com
cd YOUR_REPOSITORY_NAME
```

### 2. Install Required Dependencies
Make sure you have the required packages installed:
```bash
pip install streamlit pandas plotly folium streamlit-folium
```

### 3. Run the Application
Since the core file is named `Metsloomad.py`, execute the following command from the project root directory (e.g., your Desktop or project folder):
```bash
python -m streamlit run Metsloomad.py
```

---

## 📊 Data Source & Methodology

The application models dynamic multi-year trajectories to show realistic expansion and density shifts. The dataset simulates historical distribution metrics based on framework criteria from public ecological syntheses provided by the Estonian Environment Agency (*Keskkonnaagentuur*). 

*Note: This application is intended for demonstration and portfolio purposes.*
