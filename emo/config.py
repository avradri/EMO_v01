"""
Configuration values for EMO v0.1.

You can tweak these as needed – for example, to change file paths,
topics, or thresholds – without touching the core metric logic.
"""

from pathlib import Path

# Base directory (assumed to be the repository root when running `python main.py`)
BASE_DIR = Path(__file__).resolve().parents[1]

# Data directory
DATA_DIR = BASE_DIR / "data"

# Default CSV filenames (you can change these to match your actual files)
TREATIES_CSV = DATA_DIR / "owid_treaties.csv"
CONFLICT_CSV = DATA_DIR / "conflict_deaths.csv"

GDELT_NEWS_CSV = DATA_DIR / "gdelt_climate_news.csv"
OPENALEX_PUBS_CSV = DATA_DIR / "openalex_climate_pubs.csv"
CONFLICT_FOR_SYNERGY_CSV = DATA_DIR / "conflict_deaths_for_synergy.csv"  # optional

WIKIPEDIA_IPCC_CSV = DATA_DIR / "wikipedia_ipcc_pageviews.csv"

CO2_TARGET_CSV = DATA_DIR / "co2_target_pathway.csv"
CO2_ACTUAL_CSV = DATA_DIR / "co2_actual.csv"

ECMWF_SKILL_CSV = DATA_DIR / "ecmwf_headline_scores.csv"

# GWI defaults
GWI_TOPIC_NAME = "IPCC"
GWI_IGNITION_PERCENTILE = 95.0

# User agent string for future API calls (if you add them later)
USER_AGENT = "EMO-v0.1 (contact: your_email@example.com)"
