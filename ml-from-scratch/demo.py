"""Fit and evaluate the implemented estimators with one command: python demo.py."""

import numpy as np

from mlfs import (
    DecisionTreeClassifier,
    DecisionTreeRegressor,
    GaussianNB,
    KMeans,
    KNN,
    LinearRegression,
    LogisticRegression,
    PCA,
    RandomForestClassifier,
    RandomForestRegressor,
    StandardScaler,
)
from mlfs.metrics import mean_squared_error


def make_blobs(n_samples, centers, cluster_std=1.0, random_state=0):
    """Generate shuffled isotropic Gaussian blobs without sklearn."""
    rng = np.random.default_rng(random_state)
    centers = np.asarray(centers, dtype=float)
    counts = [n_samples // len(centers)] * len(centers)
    for index in range(n_samples - sum(counts)):
        counts[index] += 1
    features, labels = [], []
    for label, (center, count) in enumerate(zip(centers, counts)):
        features.append(rng.normal(center, cluster_std, size=(count, centers.shape[1])))
        labels.append(np.full(count, label))
    X, y = np.vstack(features), np.concatenate(labels)
    order = rng.permutation(len(y))
    return X[order], y[order]


def train_test_split(X, y, test_size=0.2, random_state=0):
    """Split arrays with a reproducible random permutation."""
    rng = np.random.default_rng(random_state)
    order = rng.permutation(len(y))
    n_test = max(1, int(round(len(y) * test_size)))
    test_idx, train_idx = order[:n_test], order[n_test:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def main() -> int:
    rng = np.random.default_rng(11)
    checks = []

    # Supervised classification: three classes, including softmax logistic regression.
    X, y = make_blobs(
        600, [[-3, -2], [3, -2], [0, 3.5]], cluster_std=0.65, random_state=7
    )
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=8)
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    classifiers = [
        ("KNN", KNN(n_neighbors=5), X_train_scaled, X_test_scaled),
        ("LogisticRegression", LogisticRegression(learning_rate=0.3, n_iters=1800), X_train_scaled, X_test_scaled),
        ("GaussianNB", GaussianNB(), X_train, X_test),
        ("DecisionTreeClassifier", DecisionTreeClassifier(max_depth=6, random_state=3), X_train, X_test),
        ("RandomForestClassifier", RandomForestClassifier(n_estimators=30, max_depth=8, random_state=3), X_train, X_test),
    ]
    print("ML from Scratch | NumPy only")
    print("=" * 66)
    for name, model, train_features, test_features in classifiers:
        model.fit(train_features, y_train)
        accuracy = model.score(test_features, y_test)
        print(f"{name:24s} accuracy = {accuracy:.4f}")
        checks.append((f"{name} classification accuracy", accuracy >= 0.88))

    # Linear regression recovers known coefficients using least squares.
    X_reg = rng.normal(size=(240, 3))
    true_coef = np.array([3.0, -2.0, 0.5])
    y_reg = X_reg @ true_coef + 1.5 + rng.normal(scale=0.2, size=len(X_reg))
    X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, random_state=9)
    linear = LinearRegression().fit(X_train, y_train)
    linear_r2 = linear.score(X_test, y_test)
    linear_rmse = float(np.sqrt(mean_squared_error(y_test, linear.predict(X_test))))
    print(f"\nLinearRegression        R² = {linear_r2:.4f}, RMSE = {linear_rmse:.4f}")
    checks.append(("linear regression recovers coefficients", np.max(np.abs(linear.coef_ - true_coef)) < 0.08))

    # Regression trees and forests fit a nonlinear signal.
    X_curve = rng.uniform(-2.0, 2.0, size=(360, 1))
    y_curve = np.sin(2.5 * X_curve[:, 0]) + rng.normal(scale=0.08, size=len(X_curve))
    X_train, X_test, y_train, y_test = train_test_split(X_curve, y_curve, random_state=10)
    for name, model in [
        ("DecisionTreeRegressor", DecisionTreeRegressor(max_depth=7, min_samples_leaf=3, random_state=5)),
        ("RandomForestRegressor", RandomForestRegressor(n_estimators=35, max_depth=8, random_state=5)),
    ]:
        model.fit(X_train, y_train)
        r2 = model.score(X_test, y_test)
        print(f"{name:24s} R² = {r2:.4f}")
        checks.append((f"{name} nonlinear fit", r2 >= 0.75))

    # Unsupervised clustering and dimensionality reduction.
    X_cluster, _ = make_blobs(
        300, [[-4, -3], [4, -3], [0, 4]], cluster_std=0.55, random_state=12
    )
    kmeans = KMeans(n_clusters=3, n_init=5, random_state=6).fit(X_cluster)
    print(f"\nKMeans                  inertia = {kmeans.inertia_:.2f}")
    checks.append(("KMeans recovers compact clusters", kmeans.inertia_ < 250.0))

    latent = rng.normal(size=(180, 2))
    X_correlated = np.column_stack(
        (latent[:, 0], latent[:, 1], latent[:, 0] + 2.0 * latent[:, 1])
    )
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(X_correlated)
    reconstruction_error = float(np.mean((pca.inverse_transform(reduced) - X_correlated) ** 2))
    print(f"PCA                     variance = {pca.explained_variance_ratio_.sum():.4f}, reconstruction MSE = {reconstruction_error:.2e}")
    checks.append(("PCA preserves the rank-2 signal", reconstruction_error < 1e-10))

    print("\n" + "-" * 66)
    for label, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    passed = sum(ok for _, ok in checks)
    print(f"  {passed}/{len(checks)} checks passed")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
