"""
Global Workspace Ignition (GWI) metric for EMO v0.1.

We combine:
- Daily news counts for a topic (e.g. "IPCC").
- Daily Wikipedia pageviews for the same topic.

We then:
- Z-score each stream.
- Define ignition = logistic(news_z + search_z).
- Flag ignition events above a high percentile (e.g. 95th).
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from .utils import zscore, logistic
from . import config


@dataclass
class GWIResult:
    time_series: pd.DataFrame
    threshold: float
    ignition_events: pd.DataFrame


def compute_gwi(
    news_df: pd.DataFrame,
    wiki_df: pd.DataFrame,
    date_col: str = "date",
    news_col: str = "news_count",
    wiki_col: str = "pageviews",
    percentile: float = None,
) -> Optional[GWIResult]:
    """
    Compute GWI score and ignition events.

    Expects daily dataframes with columns:
    - news_df: [date, news_count]
    - wiki_df: [date, pageviews]
    """
    if percentile is None:
        percentile = config.GWI_IGNITION_PERCENTILE

    # Parse dates
    df_news = news_df[[date_col, news_col]].copy()
    df_wiki = wiki_df[[date_col, wiki_col]].copy()

    df_news[date_col] = pd.to_datetime(df_news[date_col])
    df_wiki[date_col] = pd.to_datetime(df_wiki[date_col])

    df = pd.merge(df_news, df_wiki, on=date_col, how="inner").dropna()
    if df.empty:
        return None

    # Z-scores
    df["news_z"] = zscore(df[news_col])
    df["wiki_z"] = zscore(df[wiki_col])

    # Ignition: logistic of sum
    df["ignition_raw"] = df["news_z"] + df["wiki_z"]
    df["ignition"] = logistic(df["ignition_raw"].values)

    # Threshold by percentile
    thresh = np.percentile(df["ignition"], percentile)
    df["is_ignition"] = df["ignition"] >= thresh

    events = df[df["is_ignition"]].copy()

    return GWIResult(time_series=df.sort_values(date_col), threshold=float(thresh), ignition_events=events)
