"""
ingest.py — Load and clean CMS Medicare Advantage data.

Produces processed CSVs in data/processed/:
  - star_ratings.csv     : Summary star ratings 2024-2026 per contract
  - enrollment_county.csv: MA enrollment by state/county/contract (April 2026)
  - enrollment_monthly.csv: MA vs Original Medicare by state (January 2026)
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(exist_ok=True)


# ── 1. STAR RATINGS (2024, 2025, 2026) ────────────────────────────────────────

def load_summary_ratings(year: int) -> pd.DataFrame:
    folder_map = {
        2024: RAW / "star_ratings_2024",
        2025: RAW / "star_ratings_2025",
        2026: RAW / "star_ratings_2026",
    }
    folder = folder_map[year]

    # Find the Summary Ratings file (name varies slightly by year)
    files = list(folder.glob("*Summary Rat*"))
    if not files:
        raise FileNotFoundError(f"No Summary Ratings file found in {folder}")
    path = files[0]

    # Row 0 is a title row, row 1 is the real header
    df = pd.read_csv(path, skiprows=1, dtype=str)
    df.columns = df.columns.str.strip()

    # Keep only relevant columns
    keep = ["Contract Number", "Organization Marketing Name", "Parent Organization",
            "Organization Type", "SNP",
            f"{year} Part C Summary", f"{year} Part D Summary", f"{year} Overall"]
    # Some columns may not exist (e.g. Part D for MA-only contracts)
    keep = [c for c in keep if c in df.columns]
    df = df[keep].copy()

    # Rename for consistency across years
    df = df.rename(columns={
        "Contract Number": "contract_id",
        "Organization Marketing Name": "plan_name",
        "Parent Organization": "parent_org",
        "Organization Type": "org_type",
        "SNP": "snp",
        f"{year} Part C Summary": "part_c_stars",
        f"{year} Part D Summary": "part_d_stars",
        f"{year} Overall": "overall_stars",
    })

    df["year"] = year

    # Convert star columns to numeric
    for col in ["part_c_stars", "part_d_stars", "overall_stars"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with no contract ID or no star rating at all
    df = df.dropna(subset=["contract_id"])
    df = df[df["overall_stars"].notna() | df["part_c_stars"].notna()]

    return df


def build_star_ratings():
    print("Loading star ratings...")
    frames = []
    for year in [2024, 2025, 2026]:
        df = load_summary_ratings(year)
        print(f"  {year}: {len(df)} contracts")
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    out_path = OUT / "star_ratings.csv"
    combined.to_csv(out_path, index=False)
    print(f"  → saved {out_path} ({len(combined)} rows)\n")
    return combined


# ── 2. ENROLLMENT BY COUNTY (April 2026) ──────────────────────────────────────

def build_enrollment_county():
    print("Loading county enrollment...")
    path = RAW / "enrollment_2026" / "SCC_Enrollment_MA_Alt_2026_04" / "SCC_Enrollment_MA_Alt_2026_04.csv"

    df = pd.read_csv(path, dtype=str)
    df.columns = df.columns.str.strip().str.replace('"', '')

    df = df.rename(columns={
        "County": "county",
        "State": "state",
        "Contract ID": "contract_id",
        "Organization Name": "org_name",
        "Organization Type": "org_type",
        "Plan Type": "plan_type",
        "SSA Code": "ssa_code",
        "FIPS Code": "fips_code",
        "Enrolled": "enrolled",
    })

    df["enrolled"] = pd.to_numeric(df["enrolled"], errors="coerce")
    df = df.dropna(subset=["enrolled", "state"])

    out_path = OUT / "enrollment_county.csv"
    df.to_csv(out_path, index=False)
    print(f"  → saved {out_path} ({len(df)} rows)\n")
    return df


# ── 3. MONTHLY ENROLLMENT MA vs ORIGINAL (January 2026) ───────────────────────

def build_enrollment_monthly():
    print("Loading monthly enrollment...")
    path = RAW / "monthly_enrollment" / "Medicare Monthly Enrollment" / "2026-01" / \
           "Medicare Monthly Enrollment Data_January 2026.csv"

    # This file is large — read only needed columns
    df = pd.read_csv(path, dtype=str)
    df.columns = df.columns.str.strip()

    print(f"  Columns: {list(df.columns[:10])}...")
    print(f"  Shape: {df.shape}")

    out_path = OUT / "enrollment_monthly_raw.csv"
    df.to_csv(out_path, index=False)
    print(f"  → saved {out_path}\n")
    return df


# ── MAIN ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    stars = build_star_ratings()
    enroll_county = build_enrollment_county()
    enroll_monthly = build_enrollment_monthly()

    print("=== DONE ===")
    print(f"Star ratings shape:      {stars.shape}")
    print(f"County enrollment shape: {enroll_county.shape}")
    print(f"Monthly enrollment shape:{enroll_monthly.shape}")