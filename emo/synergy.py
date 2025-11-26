"""
Synergy / O-information-like indicator for EMO v0.1.

We approximate a multivariate "synergy" index using a Gaussian
covariance-based measure:

- Take 2–3 time series (news, papers, conflict).
- Log-transform, z-score.
- Build a covariance matrix Σ.
- Compute:

    synergy_index = log(det(Σ) / prod(diag(Σ)))

This is related to multi-information: if variables are independent,
det(Σ) ≈ prod(diag(Σ)), so the ratio ≈ 1 and log(...) ≈ 0.

Negative values often indicate redundancy-like structure,
positive values can indicate more complex interactions.

This is a **simple prototype**, not a full Rosas-style Ω implementation.
"""

from dataclasses import dataclass
from typing import Optional, List

import numpy as np
import pandas as pd

from .utils import zscore


@dataclass
class SynergyResult:
    synergy_index: Optional[float]
    used_columns: List[str]
    combined_df: pd.DataFrame


def compute_synergy_gaussian(
    news_df: pd.DataFrame,
    pubs_df: pd.DataFrame,
    conflict_df: Optional[pd.DataFrame] = None,
    year_col: str = "year",
) -> SynergyResult:
    """
    Compute a Gaussian synergy-like index from multiple yearly series.

    Expects:
    - news_df: [year, news_count]
    - pubs_df: [year, papers_count]
    - conflict_df (optional): [year, conflict_deaths]

    Returns
    -------
    SynergyResult
    """
    # Basic inner join on year
    df = pd.merge(
        news_df[[year_col, "news_count"]],
        pubs_df[[year_col, "papers_count"]],
        on=year_col,
        how="inner",
    )

    cols = ["news_count", "papers_count"]

    if conflict_df is not None and "conflict_deaths" in conflict_df.columns:
        df = pd.merge(df, conflict_df[[year_col, "conflict_deaths"]], on=year_col, how="inner")
        cols.append("conflict_deaths")

    if df.empty or len(df) < 3:
        return SynergyResult(synergy_index=None, used_columns=cols, combined_df=df)

    # Log and z-score
    for col in cols:
        df[col] = df[col].astype(float)
        df[f"{col}_log"] = np.log1p(df[col])
        df[f"{col}_z"] = zscore(df[f"{col}_log"])

    z_cols = [f"{c}_z" for c in cols]
    Z = df[z_cols].values

    # Covariance matrix
    cov = np.cov(Z, rowvar=False)
    diag = np.diag(cov)

    # Guard against singular matrices or zeros
    if np.any(diag <= 0):
        return SynergyResult(synergy_index=None, used_columns=cols, combined_df=df)

    det_cov = np.linalg.det(cov)
    if det_cov <= 0:
        return SynergyResult(synergy_index=None, used_columns=cols, combined_df=df)

    ratio = det_cov / np.prod(diag)
    synergy_index = float(np.log(ratio))

    return SynergyResult(synergy_index=synergy_index, used_columns=cols, combined_df=df)
