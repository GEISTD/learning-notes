"""Evaluation metrics implemented with NumPy."""

import numpy as np


def _check_pair(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if y_true.shape != y_pred.shape:
        raise ValueError(f"shape mismatch: y_true {y_true.shape}, y_pred {y_pred.shape}")
    if y_true.size == 0:
        raise ValueError("cannot score an empty array")
    return y_true, y_pred


def accuracy_score(y_true, y_pred) -> float:
    """Fraction of exactly matching labels."""
    y_true, y_pred = _check_pair(y_true, y_pred)
    return float(np.mean(y_true == y_pred))


def mean_squared_error(y_true, y_pred) -> float:
    """Average squared error."""
    y_true, y_pred = _check_pair(y_true, y_pred)
    return float(np.mean((y_true.astype(float) - y_pred.astype(float)) ** 2))


def r2_score(y_true, y_pred) -> float:
    """Coefficient of determination: 1 - SS_res / SS_tot."""
    y_true, y_pred = _check_pair(y_true, y_pred)
    y_true = y_true.astype(float)
    y_pred = y_pred.astype(float)
    ss_res = float(np.sum((y_true - y_pred) ** 2))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    if ss_tot == 0.0:
        return 1.0 if ss_res == 0.0 else 0.0
    return 1.0 - ss_res / ss_tot
