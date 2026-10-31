"""K-means clustering implemented with NumPy."""

import numpy as np

from .base import BaseEstimator, check_X, check_is_fitted


class KMeans(BaseEstimator):
    """Lloyd's K-means algorithm with k-means++ initialization and restarts."""

    def __init__(self, n_clusters=8, max_iter=300, tol=1e-4,
                 n_init=10, random_state=None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.n_init = n_init
        self.random_state = random_state

    def fit(self, X, y=None):
        X = check_X(X)
        if not np.isfinite(X).all():
            raise ValueError("X must contain only finite values")
        if not isinstance(self.n_clusters, (int, np.integer)) or self.n_clusters < 1:
            raise ValueError("n_clusters must be a positive integer")
        if self.n_clusters > len(X):
            raise ValueError("n_clusters cannot exceed the number of samples")
        if not isinstance(self.max_iter, (int, np.integer)) or self.max_iter < 1:
            raise ValueError("max_iter must be a positive integer")
        if not isinstance(self.n_init, (int, np.integer)) or self.n_init < 1:
            raise ValueError("n_init must be a positive integer")
        if not np.isfinite(self.tol) or self.tol < 0:
            raise ValueError("tol must be finite and non-negative")

        rng = np.random.default_rng(self.random_state)
        best = None
        for _restart in range(self.n_init):
            centers = self._initialize(X, rng)
            for iteration in range(self.max_iter):
                labels, distances = self._assign(X, centers)
                new_centers = centers.copy()
                for cluster in range(self.n_clusters):
                    members = X[labels == cluster]
                    if len(members):
                        new_centers[cluster] = members.mean(axis=0)
                    else:
                        # Revive an empty cluster at the least well represented point.
                        nearest_distance = np.min(distances, axis=1)
                        new_centers[cluster] = X[int(np.argmax(nearest_distance))]
                shift = float(np.sum((new_centers - centers) ** 2))
                centers = new_centers
                if shift <= self.tol**2:
                    break

            labels, distances = self._assign(X, centers)
            inertia = float(np.sum(distances[np.arange(len(X)), labels]))
            if best is None or inertia < best[0]:
                best = (inertia, centers.copy(), labels.copy(), iteration + 1)

        self.inertia_ = best[0]
        self.cluster_centers_ = best[1]
        self.labels_ = best[2]
        self.n_iter_ = best[3]
        self.n_features_in_ = X.shape[1]
        return self

    def _initialize(self, X, rng):
        centers = [X[int(rng.integers(len(X)))]]
        closest = np.sum((X - centers[0]) ** 2, axis=1)
        for _ in range(1, self.n_clusters):
            total = float(closest.sum())
            if total <= 0.0:
                # Identical observations: choose another row without replacement.
                remaining = [i for i in range(len(X)) if not any(np.array_equal(X[i], c) for c in centers)]
                index = int(rng.choice(remaining)) if remaining else int(rng.integers(len(X)))
            else:
                index = int(rng.choice(len(X), p=closest / total))
            centers.append(X[index])
            distance = np.sum((X - X[index]) ** 2, axis=1)
            closest = np.minimum(closest, distance)
        return np.asarray(centers, dtype=float)

    @staticmethod
    def _assign(X, centers):
        distances = np.sum((X[:, None, :] - centers[None, :, :]) ** 2, axis=2)
        return np.argmin(distances, axis=1), distances

    def predict(self, X):
        check_is_fitted(self)
        X = check_X(X, self.n_features_in_)
        if not np.isfinite(X).all():
            raise ValueError("X must contain only finite values")
        labels, _ = self._assign(X, self.cluster_centers_)
        return labels

    def fit_predict(self, X, y=None):
        return self.fit(X, y).labels_.copy()

    def score(self, X, y=None):
        """Return negative within-cluster sum of squared distances."""
        X = check_X(X, self.n_features_in_ if hasattr(self, "n_features_in_") else None)
        labels = self.predict(X)
        _, distances = self._assign(X, self.cluster_centers_)
        return -float(np.sum(distances[np.arange(len(X)), labels]))
