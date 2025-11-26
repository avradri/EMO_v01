"""
Small utility functions used across EMO modules.
"""

import numpy as np
import pandas as pd
from typing import Tuple


def logistic(x: np.ndarray, k: float = 1.0) -> np.ndarray:
    """
    Logistic squashing function.

    Parameters
    ----------
    x : np.ndarray
        Input array.
    k : float
        Steepness parameter.

    Returns
    -------
    np.ndarray
        Values in (0, 1).
    """
    return 1.0 / (1.0 + np.exp(-k * x))


def zscore(series: pd.Series) -> pd.Series:
    """
    Z-score a pandas Series (mean 0, std 1), ignoring NaNs.

    Returns 0 where std is 0 or series is constant.
    """
    s = series.astype(float)
    mean = s.mean()
    std = s.std()
    if std == 0 or np.isnan(std):
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - mean) / std


def simple_linear_trend(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
    """
    Fit a simple linear trend y = a * x + b using numpy.polyfit.

    Returns
    -------
    slope : float
        The trend per unit x (e.g. per year).
    intercept : float
        The intercept of the line.
    """
    if len(x) < 2:
        return 0.0, float(y[0]) if len(y) > 0 else 0.0

    # Ensure no NaNs
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 2:
        return 0.0, 0.0

    slope, intercept = np.polyfit(x[mask], y[mask], 1)
    return float(slope), float(intercept)
