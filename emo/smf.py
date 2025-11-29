"""
Self-Model Fidelity (SMF) for EMO v0.1.

Inputs:
- M(t): model / target trajectory (e.g. 1.5 °C-consistent CO₂ pathway).
- A(t): actual trajectory (e.g. realised CO₂ emissions).

We compute:
- A normalized gap g(t) = (A - M) / max(|A|, |M|, epsilon).
- SMF(t) = logistic(-|g(t)| * k) for some k, so smaller gaps -> higher SMF.
- Global SMF = mean(SMF(t)).
- Correlation between M and A.
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from .utils import logistic


@dataclass
class SMFResult:
    series: pd.DataFrame
    global_smf: Optional[float]
    correlation: Optional[float]


def compute_smf(
    target_df: pd.DataFrame,
    actual_df: pd.DataFrame,
    year_col: str = "year",
    target_col: str = "co2_target",
    actual_col: str = "co2_actual",
    k: float = 5.0,
) -> SMFResult:
    """
    Compute Self-Model Fidelity (SMF) from yearly target and actual trajectories.
    """
    t = target_df[[year_col, target_col]].copy()
    a = actual_df[[year_col, actual_col]].copy()

    df = pd.merge(t, a, on=year_col, how="inner").dropna()
    if df.empty:
        return SMFResult(series=pd.DataFrame(), global_smf=None, correlation=None)

    df[target_col] = df[target_col].astype(float)
    df[actual_col] = df[actual_col].astype(float)

    # Normalized gap
    eps = 1e-9
    denom = np.maximum(
        np.maximum(np.abs(df[target_col]), np.abs(df[actual_col])),
        eps,
    )
    df["gap_norm"] = (df[actual_col] - df[target_col]) / denom

    # SMF(t): high when |gap_norm| is small
    df["smf"] = logistic(-np.abs(df["gap_norm"].values) * k)

    global_smf = float(df["smf"].mean())

    # Correlation
    if len(df) >= 2:
        corr = float(df[[target_col, actual_col]].corr().iloc[0, 1])
    else:
        corr = None

    return SMFResult(
        series=df.sort_values(year_col),
        global_smf=global_smf,
        correlation=corr,
    )
