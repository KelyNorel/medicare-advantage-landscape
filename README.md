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
|   └── figures/      # saved plots
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

```
### Run the dashboard

```bash
streamlit run src/app.py
```

The dashboard includes four interactive views:
- **Star Rating Distribution** — histogram with mean overlay, filterable by year
- **Market Concentration** — top 15 parent organizations by contracts, colored by avg star rating
- **MA Penetration by State** — choropleth map (January 2026)
- **Plan Size vs Quality** — scatter plot of enrollment vs star rating by organization


## Key Findings

1. **Star rating quality has stagnated** — the mean overall rating (~3.65) has been 
   stable across 2024–2026, but the distribution has shifted: fewer contracts achieve 
   4+ stars, suggesting CMS has tightened its methodology.

2. **Market is highly concentrated** — UnitedHealth, Centene, CVS, and Elevance 
   account for the majority of MA contracts. Larger organizations tend to have lower 
   average ratings than smaller regional players (Kaiser ★4.3, Alignment ★4.4).

3. **MA has crossed the 50% threshold** — 27 of 51 states now have majority MA 
   enrollment. Michigan leads at 63%; Alaska is lowest at ~5%.

4. **Size and quality are modestly correlated** (Spearman r=0.36) — large plans 
   rarely fall below 3.0 stars, while small plans show the highest variance.

5. **SNP vs Non-SNP plans perform similarly** — median star rating is 3.5 for both 
   groups across all years, despite SNPs serving significantly more complex populations.

See [`notebooks/01_eda.ipynb`](notebooks/01_eda.ipynb) for the full analysis.



---

**Author:** Raquel Norel, PhD
**Domain:** Healthcare / Medicare policy
**Status:** ✅ Complete
