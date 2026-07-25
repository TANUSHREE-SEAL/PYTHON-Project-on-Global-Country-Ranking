"""
Global Country Ranking Dashboard
Built with: pandas, numpy, matplotlib, seaborn, streamlit
Run with:   streamlit run app.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import pycountry

# ----------------------------------------------------------------------
# PAGE CONFIG & STYLE
# ----------------------------------------------------------------------
st.set_page_config(page_title="Global Country Ranking Dashboard", page_icon="🌍", layout="wide")
sns.set_theme(style="whitegrid")
plt.rcParams["figure.facecolor"] = "white"

st.markdown(
    """
    <style>
    .info-box-green {
        background-color: #16342b; color: #6fe3a3; padding: 14px 16px;
        border-radius: 8px; font-weight: 600; text-align: left; margin-bottom: 10px;
    }
    .info-box-blue {
        background-color: #16283f; color: #7fb6f5; padding: 14px 16px;
        border-radius: 8px; font-weight: 600; text-align: left; margin-bottom: 10px;
    }
    .side-label { font-weight: 700; font-size: 1.05rem; margin-top: 4px; }
    .chart-title { font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/global_country_ranking.csv")
    tier_map = {1: "Tier 1 (High Income)", 2: "Tier 2 (Upper-Mid)",
                3: "Tier 3 (Lower-Mid)", 4: "Tier 4 (Low Income)"}
    df["Economic_Tier_Label"] = df["Economic_Tier"].map(tier_map)
    return df


df = load_data()

# ----------------------------------------------------------------------
# COUNTRY NAME -> ISO-3 CODE (needed for the choropleth map)
# ----------------------------------------------------------------------
ISO3_OVERRIDES = {
    "Bahamas, The": "BHS", "Brunei Darussalam": "BRN", "Cabo Verde": "CPV",
    "Congo, Dem. Rep.": "COD", "Congo, Rep.": "COG", "Cote d'Ivoire": "CIV",
    "Czechia": "CZE", "Egypt, Arab Rep.": "EGY", "Gambia, The": "GMB",
    "Hong Kong SAR, China": "HKG", "Iran, Islamic Rep.": "IRN",
    "Korea, Dem. People's Rep.": "PRK", "Korea, Rep.": "KOR",
    "Kyrgyz Republic": "KGZ", "Lao PDR": "LAO", "Macao SAR, China": "MAC",
    "Micronesia, Fed. Sts.": "FSM", "Naoero": "NRU", "Russian Federation": "RUS",
    "Slovak Republic": "SVK", "Somalia, Fed. Rep.": "SOM",
    "St. Kitts and Nevis": "KNA", "St. Lucia": "LCA",
    "St. Vincent and the Grenadines": "VCT", "Syrian Arab Republic": "SYR",
    "Turkiye": "TUR", "Venezuela, RB": "VEN", "Viet Nam": "VNM",
    "Yemen, Rep.": "YEM", "West Bank and Gaza": "PSE",
    "St. Martin (French part)": "MAF", "Sint Maarten (Dutch part)": "SXM",
    "Puerto Rico (US)": "PRI", "Virgin Islands (U.S.)": "VIR",
    "British Virgin Islands": "VGB", "United States": "USA", "Curacao": "CUW",
    "Channel Islands": None, "Kosovo": None,
}


@st.cache_data
def build_iso3_map(country_names):
    mapping = {}
    for name in country_names:
        if name in ISO3_OVERRIDES:
            mapping[name] = ISO3_OVERRIDES[name]
            continue
        try:
            mapping[name] = pycountry.countries.lookup(name).alpha_3
        except LookupError:
            mapping[name] = None
    return mapping


iso3_map = build_iso3_map(tuple(df["Country"].unique()))
df["ISO3"] = df["Country"].map(iso3_map)

RANK_COLS = [
    "Happiness_Rank", "Global_Hunger_Rank", "Human_Development_Rank",
    "GDP_Per_Capita_Rank", "Life_Expectancy_Rank", "Corruption_Perception_Rank",
    "Democracy_Rank", "Gini_Rank", "Press_Freedom_Rank",
    "Global_Peace_Rank", "Environmental_Performance_Rank",
]
# Note: for all *_Rank columns, LOWER = BETTER (rank 1 is best)

# ----------------------------------------------------------------------
# SECTIONS
# ----------------------------------------------------------------------
sections = [
    {"title": "🌍 Regional Overview",
     "charts": ["Countries by Region", "Economic Tier by Region"]},
    {"title": "😊 Happiness & Development",
     "charts": ["Avg Happiness Rank by Region", "Avg Human Development Rank by Region"]},
    {"title": "💰 Economic Indicators",
     "charts": ["Avg GDP Per Capita Rank by Region", "Avg Gini (Inequality) Rank by Region"]},
    {"title": "🏥 Life & Environment",
     "charts": ["Avg Life Expectancy Rank by Region", "Avg Environmental Performance Rank by Region"]},
    {"title": "🕊️ Governance",
     "charts": ["Avg Corruption Perception Rank by Region", "Avg Democracy Rank by Region"]},
    {"title": "📰 Freedom & Peace",
     "charts": ["Press Freedom vs Global Peace Rank", "Avg Global Peace Rank by Region"]},
    {"title": "🏆 Top Performers",
     "charts": ["Top 10 Happiest Countries (Latest Year)", "Happiness Rank Trend — Top 5 Countries"]},
]

# ----------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌍 Global Ranking Dashboard")

    st.markdown('<div class="side-label">Created By</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box-green">TANUSHREE SEAL</div>', unsafe_allow_html=True)

    st.markdown('<div class="side-label">🛠️ Tools Used</div>', unsafe_allow_html=True)
    st.markdown("- Python\n- Pandas\n- NumPy\n- Matplotlib\n- Seaborn\n- Streamlit")

    st.markdown('<div class="side-label">📊 Dataset</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="info-box-blue">{df.shape[0]:,} Records | {df["Country"].nunique()} Countries</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("**Jump to a section:**")
    for i, s in enumerate(sections, start=1):
        st.markdown(f"- [{s['title']}](#sec{i})")

# ----------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------
st.markdown("# 🌍 Global Country Ranking Dashboard")
st.markdown("### Happiness, Development, Governance & Environment Insights (2000–2026)")
st.markdown("---")

# ----------------------------------------------------------------------
# FILTERS
# ----------------------------------------------------------------------
st.markdown("## 🔍 Filters")

f1, f2, f3, f4 = st.columns(4)
with f1:
    region_sel = st.selectbox("🌎 Region", ["All"] + sorted(df["Region"].unique().tolist()))
with f2:
    tier_sel = st.selectbox("💵 Economic Tier", ["All"] + sorted(df["Economic_Tier_Label"].unique().tolist()))
with f3:
    years = sorted(df["Year"].unique().tolist())
    year_sel = st.selectbox("📅 Year", ["All Years"] + [str(y) for y in years], index=len(years))
with f4:
    country_sel = st.selectbox("🏳️ Country", ["All"] + sorted(df["Country"].unique().tolist()))

fdf = df.copy()
if region_sel != "All":
    fdf = fdf[fdf["Region"] == region_sel]
if tier_sel != "All":
    fdf = fdf[fdf["Economic_Tier_Label"] == tier_sel]
if year_sel != "All Years":
    fdf = fdf[fdf["Year"] == int(year_sel)]
if country_sel != "All":
    fdf = fdf[fdf["Country"] == country_sel]

if fdf.empty:
    st.warning("No records match the selected filters. Showing full dataset instead.")
    fdf = df.copy()

# ----------------------------------------------------------------------
# KPIs
# ----------------------------------------------------------------------
st.markdown("## 📈 Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)
k1.metric("📦 Total Records", f"{fdf.shape[0]:,}")
k2.metric("🏳️ Countries", f"{fdf['Country'].nunique()}")
k3.metric("📅 Years Covered", f"{fdf['Year'].nunique()}")
best_region = fdf.groupby("Region")["Happiness_Rank"].mean().idxmin() if not fdf.empty else "N/A"
k4.metric("😊 Happiest Region (avg)", best_region)

k5, k6, k7, k8 = st.columns(4)
k5.metric("⭐ Avg Happiness Rank", f"{fdf['Happiness_Rank'].mean():.1f}")
k6.metric("💰 Avg GDP/Capita Rank", f"{fdf['GDP_Per_Capita_Rank'].mean():.1f}")
k7.metric("🏥 Avg Life Expectancy Rank", f"{fdf['Life_Expectancy_Rank'].mean():.1f}")
k8.metric("🕊️ Avg Corruption Rank", f"{fdf['Corruption_Perception_Rank'].mean():.1f}")

st.caption("Note: for all rank metrics, a **lower number = better** (Rank 1 is the best-performing country).")
st.markdown("---")

# ----------------------------------------------------------------------
# WORLD MAP
# ----------------------------------------------------------------------
st.markdown("## 🗺️ World Map")

map_metric = st.selectbox(
    "Choose a metric to visualize on the map",
    RANK_COLS,
    format_func=lambda c: c.replace("_", " "),
)

map_year = fdf["Year"].max()
map_df = fdf[(fdf["Year"] == map_year) & (fdf["ISO3"].notna())]

if map_df.empty:
    st.info("No mappable data for the current filter selection.")
else:
    fig_map = px.choropleth(
        map_df,
        locations="ISO3",
        color=map_metric,
        hover_name="Country",
        hover_data={map_metric: True, "Region": True, "ISO3": False},
        color_continuous_scale="RdYlGn_r",  # reversed: low rank (good) = green
        projection="natural earth",
        title=f"{map_metric.replace('_', ' ')} by Country — {int(map_year)}",
    )
    fig_map.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(title="Rank<br>(lower=better)"),
        height=520,
    )
    st.plotly_chart(fig_map, use_container_width=True)
    best_row = map_df.loc[map_df[map_metric].idxmin()]
    st.caption(
        f"Showing **{map_metric.replace('_', ' ')}** for **{int(map_year)}** "
        f"(darker green = better rank). Best performer in this view: "
        f"**{best_row['Country']}** (rank {int(best_row[map_metric])})."
    )

st.markdown("---")


# ----------------------------------------------------------------------
# CHART FUNCTIONS — each returns (fig, insight_text)
# ----------------------------------------------------------------------
def chart_countries_by_region():
    s = fdf.groupby("Region")["Country"].nunique().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="viridis", legend=False, ax=ax)
    ax.set_xlabel("Number of Countries")
    ax.set_ylabel("")
    insight = f"**{s.idxmax()}** has the most countries represented in this selection ({s.max()})."
    return fig, insight


def chart_tier_by_region():
    ct = pd.crosstab(fdf["Region"], fdf["Economic_Tier_Label"])
    fig, ax = plt.subplots(figsize=(6, 5))
    ct.plot(kind="bar", stacked=True, colormap="coolwarm", ax=ax)
    ax.set_ylabel("Number of Records")
    ax.tick_params(axis="x", rotation=20)
    ax.legend(fontsize=7)
    insight = "Shows how economic tiers are distributed across regions in the current selection."
    return fig, insight


def chart_happiness_by_region():
    s = fdf.groupby("Region")["Happiness_Rank"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="mako", legend=False, ax=ax)
    ax.set_xlabel("Average Happiness Rank (lower = better)")
    ax.set_ylabel("")
    insight = f"**{s.idxmin()}** has the best (lowest) average happiness rank at {s.min():.1f}."
    return fig, insight


def chart_hdi_by_region():
    s = fdf.groupby("Region")["Human_Development_Rank"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="crest", legend=False, ax=ax)
    ax.set_xlabel("Avg Human Development Rank (lower = better)")
    ax.set_ylabel("")
    insight = f"**{s.idxmin()}** leads in human development with an average rank of {s.min():.1f}."
    return fig, insight


def chart_gdp_by_region():
    s = fdf.groupby("Region")["GDP_Per_Capita_Rank"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="rocket", legend=False, ax=ax)
    ax.set_xlabel("Avg GDP Per Capita Rank (lower = better)")
    ax.set_ylabel("")
    insight = f"**{s.idxmin()}** has the strongest average GDP-per-capita ranking ({s.min():.1f})."
    return fig, insight


def chart_gini_by_region():
    s = fdf.groupby("Region")["Gini_Rank"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="flare", legend=False, ax=ax)
    ax.set_xlabel("Avg Gini (Inequality) Rank (lower = better)")
    ax.set_ylabel("")
    insight = f"**{s.idxmin()}** shows the most equitable income distribution on average (rank {s.min():.1f})."
    return fig, insight


def chart_life_expectancy_by_region():
    s = fdf.groupby("Region")["Life_Expectancy_Rank"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="viridis", legend=False, ax=ax)
    ax.set_xlabel("Avg Life Expectancy Rank (lower = better)")
    ax.set_ylabel("")
    insight = f"**{s.idxmin()}** has the best average life-expectancy ranking ({s.min():.1f})."
    return fig, insight


def chart_environment_by_region():
    s = fdf.groupby("Region")["Environmental_Performance_Rank"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="crest", legend=False, ax=ax)
    ax.set_xlabel("Avg Environmental Performance Rank (lower = better)")
    ax.set_ylabel("")
    insight = f"**{s.idxmin()}** leads in environmental performance on average (rank {s.min():.1f})."
    return fig, insight


def chart_corruption_by_region():
    s = fdf.groupby("Region")["Corruption_Perception_Rank"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="mako", legend=False, ax=ax)
    ax.set_xlabel("Avg Corruption Perception Rank (lower = better)")
    ax.set_ylabel("")
    insight = f"**{s.idxmin()}** is perceived as least corrupt on average (rank {s.min():.1f})."
    return fig, insight


def chart_democracy_by_region():
    s = fdf.groupby("Region")["Democracy_Rank"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="rocket", legend=False, ax=ax)
    ax.set_xlabel("Avg Democracy Rank (lower = better)")
    ax.set_ylabel("")
    insight = f"**{s.idxmin()}** ranks strongest on democracy metrics on average ({s.min():.1f})."
    return fig, insight


def chart_press_vs_peace():
    corr = fdf["Press_Freedom_Rank"].corr(fdf["Global_Peace_Rank"])
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.regplot(data=fdf.sample(min(1500, len(fdf)), random_state=1), x="Press_Freedom_Rank",
                y="Global_Peace_Rank", scatter_kws={"alpha": 0.3, "s": 15}, line_kws={"color": "red"}, ax=ax)
    insight = f"Correlation between press freedom and peace ranks is **{corr:.2f}** — countries with freer press tend to rank {'better' if corr > 0.3 else 'only weakly better'} on peace."
    return fig, insight


def chart_peace_by_region():
    s = fdf.groupby("Region")["Global_Peace_Rank"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="crest", legend=False, ax=ax)
    ax.set_xlabel("Avg Global Peace Rank (lower = better)")
    ax.set_ylabel("")
    insight = f"**{s.idxmin()}** is the most peaceful region on average (rank {s.min():.1f})."
    return fig, insight


def chart_top10_happiest():
    latest_year = fdf["Year"].max()
    snap = fdf[fdf["Year"] == latest_year]
    top = snap.nsmallest(10, "Happiness_Rank")[["Country", "Happiness_Rank"]].sort_values("Happiness_Rank")
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(data=top, x="Happiness_Rank", y="Country", hue="Country", palette="Spectral", legend=False, ax=ax)
    ax.set_xlabel("Happiness Rank (lower = better)")
    insight = f"In {int(latest_year)}, **{top.iloc[0]['Country']}** holds the #{int(top.iloc[0]['Happiness_Rank'])} happiness rank."
    return fig, insight


def chart_happiness_trend_top5():
    latest_year = fdf["Year"].max()
    top5 = fdf[fdf["Year"] == latest_year].nsmallest(5, "Happiness_Rank")["Country"].tolist()
    trend = fdf[fdf["Country"].isin(top5)]
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.lineplot(data=trend, x="Year", y="Happiness_Rank", hue="Country", marker="o", ax=ax)
    ax.set_ylabel("Happiness Rank (lower = better)")
    ax.invert_yaxis()
    ax.legend(fontsize=7)
    insight = f"Tracks how this selection's top 5 happiest countries ({', '.join(top5)}) have trended over time."
    return fig, insight


chart_funcs = {
    "Countries by Region": chart_countries_by_region,
    "Economic Tier by Region": chart_tier_by_region,
    "Avg Happiness Rank by Region": chart_happiness_by_region,
    "Avg Human Development Rank by Region": chart_hdi_by_region,
    "Avg GDP Per Capita Rank by Region": chart_gdp_by_region,
    "Avg Gini (Inequality) Rank by Region": chart_gini_by_region,
    "Avg Life Expectancy Rank by Region": chart_life_expectancy_by_region,
    "Avg Environmental Performance Rank by Region": chart_environment_by_region,
    "Avg Corruption Perception Rank by Region": chart_corruption_by_region,
    "Avg Democracy Rank by Region": chart_democracy_by_region,
    "Press Freedom vs Global Peace Rank": chart_press_vs_peace,
    "Avg Global Peace Rank by Region": chart_peace_by_region,
    "Top 10 Happiest Countries (Latest Year)": chart_top10_happiest,
    "Happiness Rank Trend — Top 5 Countries": chart_happiness_trend_top5,
}

# ----------------------------------------------------------------------
# RENDER
# ----------------------------------------------------------------------
for i, sec in enumerate(sections, start=1):
    st.markdown(f'<a name="sec{i}"></a>', unsafe_allow_html=True)
    st.markdown(f"## {sec['title']}")
    col1, col2 = st.columns(2)
    for col, chart_title in zip([col1, col2], sec["charts"]):
        with col:
            st.markdown(f'<div class="chart-title">{chart_title}</div>', unsafe_allow_html=True)
            fig, insight = chart_funcs[chart_title]()
            st.pyplot(fig)
            st.caption(insight)
    st.markdown("---")

with st.expander("🔍 View raw data sample"):
    st.dataframe(fdf.head(50))
