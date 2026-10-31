"""Decision tree classifiers and regressors using CART-style binary splits."""

from dataclasses import dataclass

import numpy as np

from .base import BaseEstimator, ClassifierMixin, RegressorMixin, check_X, check_X_y, check_is_fitted


@dataclass
class _Node:
    value: object
    feature: int = -1
    threshold: float = 0.0
    left: object = None
    right: object = None

    @property
    def is_leaf(self):
        return self.feature < 0


def _validate_tree_params(max_depth, min_samples_split, min_samples_leaf, max_features):
    if max_depth is not None and (not isinstance(max_depth, (int, np.integer)) or max_depth < 0):
        raise ValueError("max_depth must be None or a non-negative integer")
    if not isinstance(min_samples_split, (int, np.integer)) or min_samples_split < 2:
        raise ValueError("min_samples_split must be an integer >= 2")
    if not isinstance(min_samples_leaf, (int, np.integer)) or min_samples_leaf < 1:
        raise ValueError("min_samples_leaf must be a positive integer")
    if max_features is not None and max_features not in ("sqrt", "log2"):
        if isinstance(max_features, (int, np.integer)):
            if max_features < 1:
                raise ValueError("integer max_features must be positive")
        elif isinstance(max_features, (float, np.floating)):
            if not 0.0 < max_features <= 1.0:
                raise ValueError("float max_features must be in (0, 1]")
        else:
            raise ValueError("max_features must be None, 'sqrt', 'log2', an int, or a float")


def _feature_count(max_features, n_features):
    if max_features is None:
        return n_features
    if max_features == "sqrt":
        return max(1, int(np.sqrt(n_features)))
    if max_features == "log2":
        return max(1, int(np.log2(n_features)))
    if isinstance(max_features, (float, np.floating)):
        return max(1, int(np.ceil(max_features * n_features)))
    if max_features > n_features:
        raise ValueError("max_features cannot exceed the number of features")
    return int(max_features)


class _DecisionTree(BaseEstimator):
    _is_classifier = False

    def __init__(self, max_depth=None, min_samples_split=2, min_samples_leaf=1,
                 max_features=None, random_state=None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.random_state = random_state

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        if not np.isfinite(X).all():
            raise ValueError("X must contain only finite values")
        if not self._is_classifier and not np.isfinite(y.astype(float)).all():
            raise ValueError("y must contain only finite numeric values for regression")
        _validate_tree_params(
            self.max_depth, self.min_samples_split, self.min_samples_leaf, self.max_features
        )
        self.n_features_in_ = X.shape[1]
        self._n_features_split = _feature_count(self.max_features, X.shape[1])
        self._rng = np.random.default_rng(self.random_state)

        if self._is_classifier:
            self.classes_, y_encoded = np.unique(y, return_inverse=True)
            if self.classes_.size < 2:
                # A one-class tree is still useful and predicts its sole class.
                self.classes_ = np.unique(y)
            target = y_encoded.astype(int)
            self.n_classes_ = len(self.classes_)
        else:
            target = y.astype(float)

        self.tree_ = self._build(X, target, depth=0)
        return self

    def _leaf_value(self, target):
        if self._is_classifier:
            counts = np.bincount(target, minlength=self.n_classes_).astype(float)
            return counts / counts.sum()
        return float(np.mean(target))

    def _impurity(self, target):
        if self._is_classifier:
            counts = np.bincount(target, minlength=self.n_classes_).astype(float)
            probabilities = counts / len(target)
            return 1.0 - float(np.sum(probabilities**2))
        return float(np.var(target))

    def _build(self, X, target, depth):
        value = self._leaf_value(target)
        node = _Node(value=value)
        if (
            self._impurity(target) <= 0.0
            or len(target) < self.min_samples_split
            or (self.max_depth is not None and depth >= self.max_depth)
        ):
            return node

        best_gain = 0.0
        best_split = None
        parent_impurity = self._impurity(target)
        features = self._rng.choice(
            self.n_features_in_, size=self._n_features_split, replace=False
        )

        for feature in features:
            order = np.argsort(X[:, feature], kind="stable")
            values = X[order, feature]
            sorted_y = target[order]
            split_positions = np.flatnonzero(values[:-1] < values[1:]) + 1
            split_positions = split_positions[
                (split_positions >= self.min_samples_leaf)
                & (len(target) - split_positions >= self.min_samples_leaf)
            ]
            if split_positions.size == 0:
                continue

            if self._is_classifier:
                cumulative = np.cumsum(
                    np.eye(self.n_classes_, dtype=float)[sorted_y], axis=0
                )
                total_counts = cumulative[-1]
                for position in split_positions:
                    left_counts = cumulative[position - 1]
                    right_counts = total_counts - left_counts
                    left_n = int(position)
                    right_n = len(target) - left_n
                    left_p = left_counts / left_n
                    right_p = right_counts / right_n
                    child_impurity = (left_n * (1.0 - left_p @ left_p)
                                      + right_n * (1.0 - right_p @ right_p)) / len(target)
                    gain = parent_impurity - child_impurity
                    if gain > best_gain:
                        best_gain = gain
                        best_split = (feature, float((values[position - 1] + values[position]) / 2.0))
            else:
                cumulative = np.cumsum(sorted_y, dtype=float)
                cumulative_sq = np.cumsum(sorted_y**2, dtype=float)
                total = cumulative[-1]
                total_sq = cumulative_sq[-1]
                for position in split_positions:
                    left_n = int(position)
                    right_n = len(target) - left_n
                    left_sum = cumulative[position - 1]
                    right_sum = total - left_sum
                    left_sse = cumulative_sq[position - 1] - left_sum**2 / left_n
                    right_sse = (total_sq - cumulative_sq[position - 1]
                                 - right_sum**2 / right_n)
                    child_impurity = max(0.0, float(left_sse + right_sse) / len(target))
                    gain = parent_impurity - child_impurity
                    if gain > best_gain:
                        best_gain = gain
                        best_split = (feature, float((values[position - 1] + values[position]) / 2.0))

        if best_split is None:
            return node
        feature, threshold = best_split
        left_mask = X[:, feature] <= threshold
        node.feature = int(feature)
        node.threshold = threshold
        node.left = self._build(X[left_mask], target[left_mask], depth + 1)
        node.right = self._build(X[~left_mask], target[~left_mask], depth + 1)
        return node

    def _leaf_for(self, row):
        node = self.tree_
        while not node.is_leaf:
            node = node.left if row[node.feature] <= node.threshold else node.right
        return node

    def _check_predict_X(self, X):
        check_is_fitted(self)
        X = check_X(X, self.n_features_in_)
        if not np.isfinite(X).all():
            raise ValueError("X must contain only finite values")
        return X


class DecisionTreeClassifier(ClassifierMixin, _DecisionTree):
    """CART decision tree classifier using Gini impurity."""

    _is_classifier = True

    def predict_proba(self, X):
        X = self._check_predict_X(X)
        return np.vstack([self._leaf_for(row).value for row in X])

    def predict(self, X):
        check_is_fitted(self)
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]


class DecisionTreeRegressor(RegressorMixin, _DecisionTree):
    """CART decision tree regressor using squared-error reduction."""

    def predict(self, X):
        X = self._check_predict_X(X)
        return np.asarray([self._leaf_for(row).value for row in X], dtype=float)
