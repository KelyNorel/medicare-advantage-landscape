# Medicare Advantage Market Landscape

Exploratory analysis of the U.S. Medicare Advantage (MA) market using publicly available CMS data.

## Overview

Medicare Advantage has grown from covering ~35% of Medicare beneficiaries in 2020 to over 50% today — 
a shift with major implications for insurers, providers, and policymakers. This project analyzes 
enrollment trends, plan quality (star ratings), and market concentration across states and major insurers.

All data sourced from CMS public datasets. No PHI involved.

## Questions Explored

1. How has MA enrollment grown by state (2020–2025)?
2. How are star ratings distributed across plans and major insurers?
3. Is there a relationship between plan size (enrollment) and quality (star rating)?
4. Which regions have the highest MA penetration vs. traditional Medicare?
5. How have star ratings changed year-over-year for major players (UnitedHealth, Humana, Aetna)?

## Data Sources

| Dataset | Source | Description |
|---|---|---|
| Monthly Enrollment by Contract | [CMS MA/Part D](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data) | Enrollment per plan, monthly |
| Star Ratings Data Tables | [CMS Part C & D Performance Data](https://www.cms.gov/medicare/health-drug-plans/part-c-d-performance-data) | Quality ratings per contract, 2024–2026 |
| Medicare Monthly Enrollment | [data.gov](https://catalog.data.gov/dataset/medicare-monthly-enrollment) | National/state/county enrollment trends |

## Stack

- Python, pandas — data ingestion and processing
- Matplotlib, seaborn — exploratory analysis (notebook)
- Plotly — interactive visualizations (dashboard)
- Streamlit — interactive web dashboard
- Jupyter — documented EDA notebook

## Project Structure
medicare-advantage-landscape/
├── data/
│   ├── raw/          # CMS source files (not tracked in git)
│   └── processed/    # cleaned datasets
├── notebooks/
│   └── 01_eda.ipynb  # exploratory data analysis
├── src/
│   ├── ingest.py     # data download and cleaning
│   └── app.py        # Streamlit dashboard
├── requirements.txt
└── README.md

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To download CMS data:
```bash
python src/ingest.py
```

To run the dashboard:
```bash
streamlit run src/app.py
```

## Results

*In progress.*

---

**Author:** Raquel Norel, PhD  
**Domain:** Healthcare / Medicare policy  
**Status:** 🚧 In progress
