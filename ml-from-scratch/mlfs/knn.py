"""k-nearest neighbours classifier implemented with NumPy."""

import numpy as np

from .base import BaseEstimator, ClassifierMixin, check_X, check_X_y, check_is_fitted


class KNN(ClassifierMixin, BaseEstimator):
    """Majority-vote k-NN classifier using Euclidean distance.

    Parameters
    ----------
    n_neighbors : int, default=5
        Number of nearest training samples that vote on each prediction.
    """

    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        if not isinstance(self.n_neighbors, (int, np.integer)) or self.n_neighbors < 1:
            raise ValueError("n_neighbors must be a positive integer")
        if self.n_neighbors > X.shape[0]:
            raise ValueError("n_neighbors cannot exceed the number of training samples")

        self.X_train_ = X
        self.y_train_ = y
        self.classes_ = np.unique(y)
        self.n_features_in_ = X.shape[1]
        return self

    def predict(self, X):
        check_is_fitted(self)
        X = check_X(X, self.n_features_in_)

        # Squared Euclidean distances expanded as |a|^2 + |b|^2 - 2ab.
        distances = (
            np.sum(X**2, axis=1)[:, None]
            + np.sum(self.X_train_**2, axis=1)[None, :]
            - 2.0 * X @ self.X_train_.T
        )
        # Floating-point round-off can produce tiny negative values.
        np.maximum(distances, 0.0, out=distances)

        nearest = np.argsort(distances, axis=1, kind="stable")[:, : self.n_neighbors]
        nearest_labels = self.y_train_[nearest]

        # Majority vote; ties go to the smallest class label.
        encoded = np.searchsorted(self.classes_, nearest_labels)
        counts = np.stack(
            [np.bincount(row, minlength=len(self.classes_)) for row in encoded]
        )
        return self.classes_[np.argmax(counts, axis=1)]
