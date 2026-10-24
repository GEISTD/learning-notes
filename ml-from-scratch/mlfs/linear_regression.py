"""Ordinary least squares linear regression implemented with NumPy."""

import numpy as np

from .base import BaseEstimator, RegressorMixin, check_X, check_X_y, check_is_fitted


class LinearRegression(RegressorMixin, BaseEstimator):
    """Ordinary least squares, solved with NumPy's SVD-based least squares.

    Parameters
    ----------
    fit_intercept : bool, default=True
        Whether to estimate an intercept term.
    """

    def __init__(self, fit_intercept=True):
        self.fit_intercept = fit_intercept

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        y = y.astype(float)

        if self.fit_intercept:
            design = np.column_stack((np.ones(X.shape[0]), X))
        else:
            design = X

        solution, *_ = np.linalg.lstsq(design, y, rcond=None)
        if self.fit_intercept:
            self.intercept_ = float(solution[0])
            self.coef_ = solution[1:]
        else:
            self.intercept_ = 0.0
            self.coef_ = solution

        self.n_features_in_ = X.shape[1]
        return self

    def predict(self, X):
        check_is_fitted(self)
        X = check_X(X, self.n_features_in_)
        return X @ self.coef_ + self.intercept_
