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
| Star Ratings Data Tables (2024–2026) | [CMS Part C & D Performance Data](https://www.cms.gov/medicare/health-drug-plans/part-c-d-performance-data) | Quality ratings per contract |
| MA Enrollment by State/County/Contract | [CMS MA Enrollment](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/monthly-ma-enrollment-state/county/contract) | Enrollment by geography, April 2026 |
| Medicare Monthly Enrollment | [data.gov](https://catalog.data.gov/dataset/medicare-monthly-enrollment) | MA vs Original Medicare by state, Jan 2026 |

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
│   └── processed/    # cleaned datasets (not tracked in git)
├── notebooks/
│   └── 01_eda.ipynb  # exploratory data analysis
├── src/
│   ├── ingest.py     # data ingestion and cleaning
│   └── app.py        # Streamlit dashboard
├── requirements.txt
└── README.md

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Download CMS data manually

Download the following files from CMS and place them in `data/raw/`:

| File | Source |
|---|---|
| 2024, 2025, 2026 Star Ratings Data Tables (ZIP) | [CMS Part C & D Performance Data](https://www.cms.gov/medicare/health-drug-plans/part-c-d-performance-data) |
| MA Enrollment by State/County/Contract — April 2026 (abridged) | [CMS MA Enrollment](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/monthly-ma-enrollment-state/county/contract) |
| Medicare Monthly Enrollment — January 2026 (dataset only) | [data.gov](https://catalog.data.gov/dataset/medicare-monthly-enrollment) |

Unzip all files into `data/raw/`, then run:

```bash
python src/ingest.py
```

This produces three clean CSVs in `data/processed/` ready for analysis:
- `star_ratings.csv` — star ratings 2024–2026 per contract
- `enrollment_county.csv` — MA enrollment by state/county/contract
- `enrollment_monthly_state.csv` — MA vs Original Medicare by state

### Run the dashboard

```bash
streamlit run src/app.py
```

## Results

*In progress.*

---

**Author:** Raquel Norel, PhD
**Domain:** Healthcare / Medicare policy
**Status:** 🚧 In progress
