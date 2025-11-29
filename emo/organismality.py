"""
Organismality Index (OI) for EMO v0.1.

Definition (simple prototype):

- Input:
  - A time series of environmental treaty participation (cooperation).
  - A time series of conflict deaths (fragmentation).

- Processing:
  - Log-transform (log1p) both series.
  - Z-score them.
  - Compute oi_raw = coop_z − violence_z.
  - Pass through logistic → OI ∈ [0, 1].

- Output:
  - A dataframe with [year, oi_raw, oi].
  - Latest value.
  - 20-year linear trend.
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from .utils import logistic, zscore, simple_linear_trend


@dataclass
class OrganismalityResult:
    series: pd.DataFrame
    latest_value: Optional[float]
    trend_20y_slope: Optional[float]


def compute_organismality(
    treaties_df: pd.DataFrame,
    conflict_df: pd.DataFrame,
    year_col: str = "year",
    treaties_col: str = "treaty_parties",
    conflict_col: str = "conflict_deaths",
) -> OrganismalityResult:
    """
    Compute the Organismality Index (OI).

    Parameters
    ----------
    treaties_df : pd.DataFrame
        Must contain [year_col, treaties_col].
    conflict_df : pd.DataFrame
        Must contain [year_col, conflict_col].

    Returns
    -------
    OrganismalityResult
    """
    # Select and align on year
    t = treaties_df[[year_col, treaties_col]].copy()
    c = conflict_df[[year_col, conflict_col]].copy()

    df = pd.merge(t, c, on=year_col, how="inner").dropna()
    if df.empty:
        return OrganismalityResult(
            series=pd.DataFrame(), latest_value=None, trend_20y_slope=None
        )

    # Log-transform
    df["coop_log"] = np.log1p(df[treaties_col].astype(float))
    df["violence_log"] = np.log1p(df[conflict_col].astype(float))

    # Z-score
    df["coop_z"] = zscore(df["coop_log"])
    df["violence_z"] = zscore(df["violence_log"])

    # Raw OI and logistic squashing
    df["oi_raw"] = df["coop_z"] - df["violence_z"]
    df["oi"] = logistic(df["oi_raw"].values)

    # Trend over the last 20 years, if possible
    df_sorted = df.sort_values(year_col)
    years = df_sorted[year_col].values.astype(float)
    oi_vals = df_sorted["oi"].values.astype(float)

    if len(df_sorted) >= 2:
        max_year = years.max()
        mask_20 = years >= (max_year - 19)
        slope, _ = simple_linear_trend(years[mask_20], oi_vals[mask_20])
        trend_slope = slope
    else:
        trend_slope = None

    latest_value = float(df_sorted.iloc[-1]["oi"])

    return OrganismalityResult(
        series=df_sorted, latest_value=latest_value, trend_20y_slope=trend_slope
    )
