"""Binary logistic regression trained with full-batch gradient descent."""

import numpy as np

from .base import BaseEstimator, ClassifierMixin, check_X, check_X_y, check_is_fitted


def _sigmoid(z):
    """Numerically safe logistic function."""
    return 1.0 / (1.0 + np.exp(-np.clip(z, -500.0, 500.0)))


class LogisticRegression(ClassifierMixin, BaseEstimator):
    """Binary logistic regression with optional L2 regularization.

    Parameters
    ----------
    learning_rate : float, default=0.1
        Step size for full-batch gradient descent.
    n_iters : int, default=2000
        Number of gradient descent iterations.
    l2 : float, default=0.0
        L2 penalty strength applied to the coefficients.
    """

    def __init__(self, learning_rate=0.1, n_iters=2000, l2=0.0):
        self.learning_rate = learning_rate
        self.n_iters = n_iters
        self.l2 = l2

    def fit(self, X, y):
        X, y = check_X_y(X, y)
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if not isinstance(self.n_iters, (int, np.integer)) or self.n_iters < 1:
            raise ValueError("n_iters must be a positive integer")
        if self.l2 < 0:
            raise ValueError("l2 must be non-negative")

        self.classes_ = np.unique(y)
        if self.classes_.size != 2:
            raise ValueError("LogisticRegression supports exactly two classes")
        y_binary = (y == self.classes_[1]).astype(float)

        n_samples, n_features = X.shape
        self.coef_ = np.zeros(n_features)
        self.intercept_ = 0.0
        self.loss_history_ = []

        for _ in range(self.n_iters):
            probabilities = _sigmoid(X @ self.coef_ + self.intercept_)
            errors = probabilities - y_binary

            grad_coef = X.T @ errors / n_samples + self.l2 * self.coef_
            grad_intercept = float(np.mean(errors))

            self.coef_ -= self.learning_rate * grad_coef
            self.intercept_ -= self.learning_rate * grad_intercept

            clipped = np.clip(probabilities, 1e-12, 1.0 - 1e-12)
            loss = -np.mean(
                y_binary * np.log(clipped) + (1.0 - y_binary) * np.log(1.0 - clipped)
            )
            loss += 0.5 * self.l2 * float(np.sum(self.coef_**2))
            self.loss_history_.append(float(loss))

        self.n_features_in_ = n_features
        return self

    def predict_proba(self, X):
        """Return probabilities for [negative class, positive class]."""
        check_is_fitted(self)
        X = check_X(X, self.n_features_in_)
        positive = _sigmoid(X @ self.coef_ + self.intercept_)
        return np.column_stack((1.0 - positive, positive))

    def predict(self, X):
        positive = self.predict_proba(X)[:, 1]
        return self.classes_[(positive >= 0.5).astype(int)]
