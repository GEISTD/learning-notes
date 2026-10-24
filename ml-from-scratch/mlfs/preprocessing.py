"""Preprocessing utilities implemented with NumPy."""

import numpy as np

from .base import check_X, check_is_fitted


class StandardScaler:
    """Standardize features using the mean and std of the training data."""

    def fit(self, X):
        X = check_X(X)
        self.mean_ = X.mean(axis=0)
        self.scale_ = X.std(axis=0)
        # Constant columns carry no information; keep them at zero instead of NaN.
        self.scale_[self.scale_ == 0.0] = 1.0
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        check_is_fitted(self)
        X = check_X(X, self.n_features_in_)
        return (X - self.mean_) / self.scale_

    def fit_transform(self, X):
        return self.fit(X).transform(X)
