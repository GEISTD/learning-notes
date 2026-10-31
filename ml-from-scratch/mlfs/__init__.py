"""Classic machine-learning estimators implemented with NumPy from scratch."""

from .base import BaseEstimator, ClassifierMixin, RegressorMixin
from .cluster import KMeans
from .decomposition import PCA
from .ensemble import RandomForestClassifier, RandomForestRegressor
from .knn import KNN
from .linear_regression import LinearRegression
from .logistic_regression import LogisticRegression
from .naive_bayes import GaussianNB
from .preprocessing import StandardScaler
from .tree import DecisionTreeClassifier, DecisionTreeRegressor

__all__ = [
    "BaseEstimator",
    "ClassifierMixin",
    "RegressorMixin",
    "KNN",
    "LinearRegression",
    "LogisticRegression",
    "GaussianNB",
    "DecisionTreeClassifier",
    "DecisionTreeRegressor",
    "RandomForestClassifier",
    "RandomForestRegressor",
    "KMeans",
    "PCA",
    "StandardScaler",
]

__version__ = "0.2.0"
