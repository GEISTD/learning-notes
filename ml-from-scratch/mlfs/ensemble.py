"""Bagged random forests built from the project's decision trees."""

import numpy as np

from .base import BaseEstimator, ClassifierMixin, RegressorMixin, check_X, check_X_y, check_is_fitted
from .tree import (
    DecisionTreeClassifier,
    DecisionTreeRegressor,
    _feature_count,
    _validate_tree_params,
)


class _RandomForest(BaseEstimator):
    _is_classifier = False

    def __init__(self, n_estimators=100, max_depth=None, min_samples_split=2,
                 min_samples_leaf=1, max_features=None, bootstrap=True,
                 random_state=None):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.bootstrap = bootstrap
        self.random_state = random_state

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        if not isinstance(self.n_estimators, (int, np.integer)) or self.n_estimators < 1:
            raise ValueError("n_estimators must be a positive integer")
        if not isinstance(self.bootstrap, (bool, np.bool_)):
            raise ValueError("bootstrap must be a boolean")
        _validate_tree_params(
            self.max_depth, self.min_samples_split,
            self.min_samples_leaf, self.max_features,
        )
        self.n_features_in_ = X.shape[1]
        self._n_features_split = _feature_count(self.max_features, X.shape[1])
        rng = np.random.default_rng(self.random_state)
        self.estimators_ = []
        n_samples = len(y)
        for _ in range(self.n_estimators):
            indices = (rng.integers(0, n_samples, size=n_samples)
                       if self.bootstrap else rng.permutation(n_samples))
            tree_seed = int(rng.integers(0, np.iinfo(np.int32).max))
            tree_type = DecisionTreeClassifier if self._is_classifier else DecisionTreeRegressor
            tree = tree_type(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                min_samples_leaf=self.min_samples_leaf,
                max_features=self.max_features,
                random_state=tree_seed,
            ).fit(X[indices], y[indices])
            self.estimators_.append(tree)

        if self._is_classifier:
            self.classes_ = np.unique(y)
        return self

    def _check_predict_X(self, X):
        check_is_fitted(self)
        X = check_X(X, self.n_features_in_)
        if not np.isfinite(X).all():
            raise ValueError("X must contain only finite values")
        return X


class RandomForestClassifier(ClassifierMixin, _RandomForest):
    """Random forest classifier with bootstrap samples and feature subsampling."""

    _is_classifier = True

    def __init__(self, n_estimators=100, max_depth=None, min_samples_split=2,
                 min_samples_leaf=1, max_features="sqrt", bootstrap=True,
                 random_state=None):
        super().__init__(n_estimators, max_depth, min_samples_split,
                         min_samples_leaf, max_features, bootstrap, random_state)

    def predict_proba(self, X):
        X = self._check_predict_X(X)
        probabilities = np.zeros((len(X), len(self.classes_)), dtype=float)
        for tree in self.estimators_:
            tree_probabilities = tree.predict_proba(X)
            class_indices = np.searchsorted(self.classes_, tree.classes_)
            probabilities[:, class_indices] += tree_probabilities
        return probabilities / len(self.estimators_)

    def predict(self, X):
        check_is_fitted(self)
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]


class RandomForestRegressor(RegressorMixin, _RandomForest):
    """Random forest regressor; predictions average the fitted tree outputs."""

    def __init__(self, n_estimators=100, max_depth=None, min_samples_split=2,
                 min_samples_leaf=1, max_features=1.0, bootstrap=True,
                 random_state=None):
        super().__init__(n_estimators, max_depth, min_samples_split,
                         min_samples_leaf, max_features, bootstrap, random_state)

    def predict(self, X):
        X = self._check_predict_X(X)
        return np.mean([tree.predict(X) for tree in self.estimators_], axis=0)
