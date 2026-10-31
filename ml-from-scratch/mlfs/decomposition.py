"""Principal component analysis using NumPy's singular value decomposition."""

import numpy as np

from .base import check_X, check_is_fitted


class PCA:
    """Project data onto principal components learned from centered features.

    ``n_components`` may be an integer component count or a float in (0, 1]
    specifying the minimum cumulative explained-variance fraction to retain.
    """

    def __init__(self, n_components=None):
        self.n_components = n_components

    def fit(self, X, y=None):
        X = check_X(X)
        if not np.isfinite(X).all():
            raise ValueError("X must contain only finite values")
        max_components = min(X.shape)
        if self.n_components is None:
            requested = max_components
        elif isinstance(self.n_components, (int, np.integer)):
            if not 1 <= self.n_components <= max_components:
                raise ValueError(f"n_components must be in [1, {max_components}]")
            requested = int(self.n_components)
        elif isinstance(self.n_components, (float, np.floating)):
            if not 0.0 < self.n_components <= 1.0:
                raise ValueError("float n_components must be in (0, 1]")
            requested = None
        else:
            raise ValueError("n_components must be None, an integer, or a float in (0, 1]")

        self.mean_ = X.mean(axis=0)
        centered = X - self.mean_
        _, singular_values, components = np.linalg.svd(centered, full_matrices=False)
        explained_variance = singular_values**2 / max(X.shape[0] - 1, 1)
        total_variance = float(explained_variance.sum())
        if total_variance == 0.0:
            ratios = np.zeros_like(explained_variance)
        else:
            ratios = explained_variance / total_variance

        if requested is None:
            requested = min(
                len(ratios),
                int(np.searchsorted(np.cumsum(ratios), self.n_components) + 1),
            )
        self.n_components_ = requested
        self.components_ = components[:requested]
        self.explained_variance_ = explained_variance[:requested]
        self.explained_variance_ratio_ = ratios[:requested]
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        check_is_fitted(self)
        X = check_X(X, self.n_features_in_)
        if not np.isfinite(X).all():
            raise ValueError("X must contain only finite values")
        return (X - self.mean_) @ self.components_.T

    def inverse_transform(self, X):
        check_is_fitted(self)
        X = check_X(X, self.n_components_)
        if not np.isfinite(X).all():
            raise ValueError("X must contain only finite values")
        return X @ self.components_ + self.mean_

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)
