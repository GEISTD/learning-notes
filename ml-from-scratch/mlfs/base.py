"""Unified estimator interface shared by every model in this project."""

from abc import ABC, abstractmethod

import numpy as np


def check_X(X, n_features=None):
    """Return X as a validated 2-D float array."""
    X = np.asarray(X, dtype=float)
    if X.ndim != 2:
        raise ValueError(f"X must be 2-D, got shape {X.shape}")
    if X.shape[0] == 0 or X.shape[1] == 0:
        raise ValueError("X must contain at least one sample and one feature")
    if n_features is not None and X.shape[1] != n_features:
        raise ValueError(f"X has {X.shape[1]} features, expected {n_features}")
    return X


def check_X_y(X, y):
    """Return validated (X, y); X becomes float, y keeps its original dtype."""
    X = check_X(X)
    y = np.asarray(y)
    if y.ndim != 1:
        raise ValueError(f"y must be 1-D, got shape {y.shape}")
    if y.shape[0] != X.shape[0]:
        raise ValueError(f"X has {X.shape[0]} samples but y has {y.shape[0]}")
    return X, y


def check_is_fitted(estimator):
    """Raise a clear error when predict is called before fit."""
    if not hasattr(estimator, "n_features_in_"):
        raise RuntimeError(
            f"{type(estimator).__name__} is not fitted yet; call fit() first"
        )


class BaseEstimator(ABC):
    """Minimal scikit-learn-style contract: fit -> predict -> score.

    Every fitted attribute ends with an underscore, so ``get_params`` can
    return only the constructor hyperparameters.
    """

    estimator_type = "estimator"

    @abstractmethod
    def fit(self, X, y):
        """Fit the model and return self."""

    @abstractmethod
    def predict(self, X):
        """Return predictions for X."""

    def score(self, X, y):
        """Return the default metric for this estimator."""
        raise NotImplementedError(f"{type(self).__name__} does not define score()")

    def get_params(self) -> dict:
        """Return constructor hyperparameters."""
        return {name: value for name, value in vars(self).items() if not name.endswith("_")}

    def __repr__(self):
        params = ", ".join(f"{name}={value!r}" for name, value in self.get_params().items())
        return f"{type(self).__name__}({params})"


class ClassifierMixin:
    """Default score for classifiers: accuracy."""

    estimator_type = "classifier"

    def score(self, X, y) -> float:
        from .metrics import accuracy_score

        return accuracy_score(y, self.predict(X))


class RegressorMixin:
    """Default score for regressors: coefficient of determination (R^2)."""

    estimator_type = "regressor"

    def score(self, X, y) -> float:
        from .metrics import r2_score

        return r2_score(y, self.predict(X))
