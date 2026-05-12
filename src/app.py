"""
app.py — Medicare Advantage Market Landscape Dashboard
Interactive Streamlit dashboard built on CMS public data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Medicare Advantage Market Landscape",
    page_icon="🏥",
    layout="wide"
)

# ── Data loading ──────────────────────────────────────────────────────────────
DATA = Path("data/processed")

@st.cache_data
def load_data():
    stars = pd.read_csv(DATA / "star_ratings.csv")
    county = pd.read_csv(DATA / "enrollment_county.csv")
    monthly = pd.read_csv(DATA / "enrollment_monthly_state.csv")
    
    # Clean strings
    for col in stars.select_dtypes("object").columns:
        stars[col] = stars[col].str.strip()
    
    return stars, county, monthly

stars, county, monthly = load_data()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏥 Medicare Advantage Market Landscape")
st.markdown("Exploratory analysis of the U.S. Medicare Advantage market using CMS public data.")
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("Filters")
year = st.sidebar.selectbox("Star Ratings Year", [2024, 2025, 2026], index=2)

# ── KPI metrics ───────────────────────────────────────────────────────────────
stars_year = stars[stars["year"] == year]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Contracts", f"{len(stars_year):,}")
col2.metric("Mean Star Rating", f"{stars_year['overall_stars'].mean():.2f}")
col3.metric("5-Star Contracts", f"{(stars_year['overall_stars'] == 5.0).sum()}")
col4.metric("Contracts ≥ 4 Stars", f"{(stars_year['overall_stars'] >= 4.0).sum()}")

st.divider()

# ── Section 1: Star Rating Distribution ───────────────────────────────────────
st.subheader("⭐ Star Rating Distribution")

fig = px.histogram(
    stars_year.dropna(subset=["overall_stars"]),
    x="overall_stars",
    nbins=9,
    color_discrete_sequence=["steelblue"],
    labels={"overall_stars": "Overall Star Rating", "count": "Number of Contracts"},
    title=f"Distribution of Overall Star Ratings ({year})"
)
fig.update_traces(xbins=dict(start=1.75, end=5.25, size=0.5))
fig.add_vline(x=stars_year["overall_stars"].mean(), 
              line_dash="dash", line_color="red",
              annotation_text=f"Mean: {stars_year['overall_stars'].mean():.2f}")
fig.update_layout(showlegend=False, height=400)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Section 2: Market Concentration ───────────────────────────────────────────
st.subheader("🏢 Market Concentration — Top 15 Parent Organizations")

top_orgs = (stars_year
            .groupby("parent_org")
            .agg(n_contracts=("contract_id", "count"),
                 avg_stars=("overall_stars", "mean"))
            .sort_values("n_contracts", ascending=False)
            .head(15)
            .reset_index())

fig2 = px.bar(top_orgs, x="n_contracts", y="parent_org",
              orientation="h",
              color="avg_stars",
              color_continuous_scale="RdYlGn",
              range_color=[2.5, 5.0],
              labels={"n_contracts": "Number of Contracts", 
                      "parent_org": "",
                      "avg_stars": "Avg Stars"},
              title=f"Top 15 MA Organizations by Number of Contracts ({year})")
fig2.update_layout(yaxis={"categoryorder": "total ascending"}, height=500)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Section 3: MA Penetration by State ────────────────────────────────────────
st.subheader("🗺️ MA Penetration by State")

exclude = ["PR", "VI", "GU", "MP", "AS", "XX", "ZZ", "UK", "FO"]
state_pen = (monthly[monthly["YEAR"] == 2026]
             .groupby("BENE_STATE_ABRVTN")
             .agg(total=("TOT_BENES", "sum"), ma=("MA_AND_OTH_BENES", "sum"))
             .assign(ma_penetration=lambda x: x["ma"] / x["total"])
             .reset_index()
             .rename(columns={"BENE_STATE_ABRVTN": "state"}))
state_pen = state_pen[~state_pen["state"].isin(exclude)]

fig3 = px.choropleth(
    state_pen,
    locations="state",
    locationmode="USA-states",
    color="ma_penetration",
    scope="usa",
    color_continuous_scale="Blues",
    range_color=[0, 0.7],
    labels={"ma_penetration": "MA Penetration"},
    title="Medicare Advantage Penetration by State (January 2026)"
)
fig3.update_layout(height=450)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ── Section 4: Enrollment vs Star Rating ──────────────────────────────────────
st.subheader("📊 Plan Size vs Quality")

enroll_by_contract = (county.groupby("contract_id")["enrolled"]
                      .sum().reset_index()
                      .rename(columns={"enrolled": "total_enrolled"}))


stars_year2 = stars[stars["year"] == year].copy()
stars_year2["contract_id"] = stars_year2["contract_id"].str.strip()
merged = stars_year2.merge(enroll_by_contract, on="contract_id", how="inner")
merged["parent_org_short"] = merged["parent_org"].str.split(",").str[0]

top8 = merged["parent_org_short"].value_counts().head(8).index.tolist()
merged["org_label"] = merged["parent_org_short"].apply(
    lambda x: x if x in top8 else "Other")

merged_plot = merged.dropna(subset=["overall_stars"]).copy()
# Add vertical jitter to separate overlapping points
np.random.seed(42)
merged_plot["stars_jitter"] = merged_plot["overall_stars"] + np.random.uniform(-0.15, 0.15, len(merged_plot))

fig4 = px.scatter(
    merged_plot,
    x="total_enrolled",
    y="stars_jitter",
    color="org_label",
    hover_data=["plan_name", "total_enrolled", "overall_stars"],
    log_x=True,
    opacity=0.6,
    labels={"total_enrolled": "Total Enrollment (log scale)",
            "stars_jitter": "Overall Star Rating",
            "org_label": "Organization"},
    title=f"Plan Enrollment vs Star Rating ({year}) — jitter added for visibility",
    category_orders={"org_label": top8 + ["Other"]}
)
fig4.add_hline(y=4.0, line_dash="dash", line_color="red",
               annotation_text="4-star threshold")
fig4.update_layout(height=500,
                   yaxis=dict(tickvals=[2, 2.5, 3, 3.5, 4, 4.5, 5],
                              ticktext=["2", "2.5", "3", "3.5", "4", "4.5", "5"]))
st.plotly_chart(fig4, use_container_width=True)
st.caption("""
**How to read this chart:** Each dot is one MA contract. The X-axis uses a log scale — 
each gridline represents a 10x increase in enrollment. Jitter has been added vertically 
so overlapping points are visible. The dashed red line marks the 4-star threshold, 
above which CMS awards quality bonus payments.

**Key insight:** Size doesn't guarantee quality, but quality is required to stay large. 
Plans below 3.0 stars are almost exclusively small — low-quality large plans lose 
enrollment over time and either shrink or exit the market.
""")

