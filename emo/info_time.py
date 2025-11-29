"""
Information-time (τ_I) for EMO v0.1.

Inputs:
- Yearly forecast skill series, e.g. ECMWF "headline scores".

We define:
- Δskill(t) = skill(t) - skill(t-1).
- τ_I(t) = sum of positive Δskill up to time t (no penalty for regressions).
- Information-time span = τ_I(end) - τ_I(start).
- Calendar span = year_end - year_start.
- Acceleration ratio = (τ_I span) / (calendar span).

This is a UIA-flavoured dI/dt proxy.
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


@dataclass
class InfoTimeResult:
    series: pd.DataFrame
    tau_span: Optional[float]
    calendar_span: Optional[float]
    accel_ratio: Optional[float]


def compute_info_time(
    skill_df: pd.DataFrame,
    year_col: str = "year",
    skill_col: str = "skill",
) -> InfoTimeResult:
    """
    Compute information-time τ_I from a yearly skill dataframe.
    """
    df = skill_df[[year_col, skill_col]].copy().dropna()
    if df.empty or len(df) < 2:
        return InfoTimeResult(
            series=pd.DataFrame(),
            tau_span=None,
            calendar_span=None,
            accel_ratio=None,
        )

    df[year_col] = df[year_col].astype(int)
    df[skill_col] = df[skill_col].astype(float)
    df = df.sort_values(year_col)

    # Year-on-year differences
    df["skill_diff"] = df[skill_col].diff()
    df["skill_gain_pos"] = df["skill_diff"].clip(lower=0.0).fillna(0.0)

    # Cumulative τ_I
    df["tau_I"] = df["skill_gain_pos"].cumsum()

    tau_span = float(df["tau_I"].iloc[-1] - df["tau_I"].iloc[0])
    year_start = int(df[year_col].iloc[0])
    year_end = int(df[year_col].iloc[-1])
    calendar_span = float(year_end - year_start) if year_end > year_start else None

    if calendar_span is None or calendar_span <= 0:
        accel_ratio = None
    else:
        accel_ratio = tau_span / calendar_span

    return InfoTimeResult(
        series=df,
        tau_span=tau_span,
        calendar_span=calendar_span,
        accel_ratio=accel_ratio,
    )
