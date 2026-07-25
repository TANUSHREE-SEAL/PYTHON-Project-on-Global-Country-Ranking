# PYTHON-Project-on-Global-Country-Ranking
# 🌍 Global Country Ranking Dashboard

An interactive dashboard exploring how countries around the world compare on happiness, development, economics, governance, and the environment — built with Python and Streamlit.

🔗 **Live Dashboard:** https://python-project-on-global-country-ranking-khnwyuf4jrmhvahsus2e8.streamlit.app/
---

## 📊 Overview

This dashboard analyzes country-level ranking data across **217 countries** from **2000–2026**, answering questions like:

- Which regions rank happiest, healthiest, and most developed?
- How do economic tiers relate to human development and inequality?
- Which countries are perceived as least corrupt or most democratic?
- Is there a relationship between press freedom and global peace?
- Which countries lead the world on each ranking, and how have they trended over time?

It includes live filters, KPI cards, an interactive world map, and 14 charts grouped into 7 analysis sections — each with a short data-driven insight.

**Note:** For every ranking metric in this dataset, a **lower number = better** performance (Rank 1 is the best-performing country).

---

## 🛠️ Tools Used

- **Python**
- **Pandas** — data cleaning & aggregation
- **NumPy** — numerical operations
- **Matplotlib** & **Seaborn** — data visualization
- **Plotly** — interactive choropleth world map
- **pycountry** — country name → ISO-3 code mapping for the map
- **Streamlit** — interactive web app framework

---

## ✨ Features

- 🔍 **Filters** — Region, Economic Tier, Year, Country
- 📈 **KPIs** — total records, countries, years covered, happiest region, average happiness/GDP/life-expectancy/corruption ranks
- 🗺️ **Interactive World Map** — choropleth map with a metric selector (choose any of 11 ranking indicators to visualize by country)
- 📊 **7 chart sections** (2 charts per section):
  - Regional Overview
  - Happiness & Development
  - Economic Indicators
  - Life & Environment
  - Governance
  - Freedom & Peace
  - Top Performers

---

## 📁 Project Structure

```
global-country-dashboard/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Python dependencies
└── data/
    └── global_country_ranking.csv  # Dataset
```

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/global-country-dashboard.git
cd global-country-dashboard
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

If `streamlit` isn't recognized directly on Windows, use:
```bash
python -m streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## ☁️ Deployment

This app is deployed on [Streamlit Community Cloud](https://share.streamlit.io):

1. Push the project to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select the repo, branch (`main`), and main file (`app.py`)
4. Click **Deploy**

---

## 📌 Dataset

`global_country_ranking.csv` contains country-year level records across 11 global ranking indices: Happiness, Global Hunger, Human Development, GDP Per Capita, Life Expectancy, Corruption Perception, Democracy, Gini (Inequality), Press Freedom, Global Peace, and Environmental Performance — plus Region and Economic Tier classifications.

---

## 👤 Author

**Tanushree Seal**
