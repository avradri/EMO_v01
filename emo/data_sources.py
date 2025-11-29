"""
Data loading helpers for EMO v0.1.

These functions assume CSV files in the `data/` directory with simple
structures. You can adapt them as needed.

Example CSV schemas:

1. owid_treaties.csv
   year,treaty_parties

2. conflict_deaths.csv
   year,conflict_deaths

3. gdelt_climate_news.csv
   year,news_count

4. openalex_climate_pubs.csv
   year,papers_count

5. wikipedia_ipcc_pageviews.csv
   date,pageviews

6. gdelt_ipcc_daily.csv
   date,news_count

7. co2_target_pathway.csv
   year,co2_target

8. co2_actual.csv
   year,co2_actual

9. ecmwf_headline_scores.csv
   year,skill
"""

from typing import Optional, Tuple

import pandas as pd

from . import config


def _load_csv(path) -> Optional[pd.DataFrame]:
    """
    Internal helper to load a CSV if it exists, else return None.
    """
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        print(f"[WARN] CSV not found: {path}")
        return None


def load_treaties() -> Optional[pd.DataFrame]:
    return _load_csv(config.TREATIES_CSV)


def load_conflict() -> Optional[pd.DataFrame]:
    return _load_csv(config.CONFLICT_CSV)


def load_synergy_streams() -> Tuple[
    Optional[pd.DataFrame],
    Optional[pd.DataFrame],
    Optional[pd.DataFrame],
]:
    """
    Load yearly streams for synergy / O-information-like metric.

    Returns
    -------
    (news_df, pubs_df, conflict_df)
    """
    news = _load_csv(config.GDELT_NEWS_CSV)
    pubs = _load_csv(config.OPENALEX_PUBS_CSV)
    conflict = _load_csv(config.CONFLICT_FOR_SYNERGY_CSV)
    return news, pubs, conflict


def load_gwi_streams() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    Returns two dataframes for GWI:
    - news_df: with columns [date, news_count]
    - wiki_df: with columns [date, pageviews]
    """
    news = _load_csv(config.GDELT_NEWS_DAILY_CSV)
    wiki = _load_csv(config.WIKIPEDIA_IPCC_CSV)
    return news, wiki


def load_co2_target() -> Optional[pd.DataFrame]:
    return _load_csv(config.CO2_TARGET_CSV)


def load_co2_actual() -> Optional[pd.DataFrame]:
    return _load_csv(config.CO2_ACTUAL_CSV)


def load_ecmwf_skill() -> Optional[pd.DataFrame]:
    return _load_csv(config.ECMWF_SKILL_CSV)
