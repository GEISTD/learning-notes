"""Three classic ML models built from scratch with a unified interface."""

from .base import BaseEstimator, ClassifierMixin, RegressorMixin
from .knn import KNN
from .linear_regression import LinearRegression
from .logistic_regression import LogisticRegression
from .preprocessing import StandardScaler

__all__ = [
    "BaseEstimator",
    "ClassifierMixin",
    "RegressorMixin",
    "KNN",
    "LinearRegression",
    "LogisticRegression",
    "StandardScaler",
]

__version__ = "0.1.0"
