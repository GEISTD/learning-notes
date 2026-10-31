"""Gaussian naive Bayes classifier implemented with NumPy."""

import numpy as np

from .base import BaseEstimator, ClassifierMixin, check_X, check_X_y, check_is_fitted


class GaussianNB(ClassifierMixin, BaseEstimator):
    """Classification using class-conditional Gaussian feature likelihoods.

    ``var_smoothing`` adds a small global variance floor so constant features
    do not cause division-by-zero or log-of-zero errors.
    """

    def __init__(self, var_smoothing=1e-9):
        self.var_smoothing = var_smoothing

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        if not np.isfinite(X).all():
            raise ValueError("X must contain only finite values")
        if not np.isfinite(self.var_smoothing) or self.var_smoothing < 0:
            raise ValueError("var_smoothing must be finite and non-negative")

        self.classes_, encoded = np.unique(y, return_inverse=True)
        if self.classes_.size < 2:
            raise ValueError("GaussianNB requires at least two classes")
        n_classes = len(self.classes_)
        n_features = X.shape[1]
        self.theta_ = np.empty((n_classes, n_features), dtype=float)
        self.var_ = np.empty_like(self.theta_)
        counts = np.bincount(encoded, minlength=n_classes)
        self.class_prior_ = counts / counts.sum()
        epsilon = max(
            self.var_smoothing * max(float(np.var(X)), 1.0),
            np.finfo(float).eps,
        )

        for index in range(n_classes):
            class_X = X[encoded == index]
            self.theta_[index] = class_X.mean(axis=0)
            self.var_[index] = class_X.var(axis=0) + epsilon

        self.n_features_in_ = n_features
        return self

    def predict_log_proba(self, X):
        check_is_fitted(self)
        X = check_X(X, self.n_features_in_)
        if not np.isfinite(X).all():
            raise ValueError("X must contain only finite values")
        log_likelihood = -0.5 * np.sum(
            np.log(2.0 * np.pi * self.var_)[None, :, :]
            + (X[:, None, :] - self.theta_[None, :, :]) ** 2
            / self.var_[None, :, :],
            axis=2,
        )
        joint = log_likelihood + np.log(self.class_prior_)[None, :]
        maximum = np.max(joint, axis=1, keepdims=True)
        return joint - maximum - np.log(np.sum(np.exp(joint - maximum), axis=1, keepdims=True))

    def predict_proba(self, X):
        return np.exp(self.predict_log_proba(X))

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_log_proba(X), axis=1)]
