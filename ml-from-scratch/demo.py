"""Train and evaluate all three models with one command: python demo.py."""

import numpy as np

from mlfs import KNN, LinearRegression, LogisticRegression, StandardScaler
from mlfs.metrics import mean_squared_error


def make_blobs(n_samples, centers, cluster_std=1.0, random_state=0):
    """Generate isotropic Gaussian blobs for classification."""
    rng = np.random.default_rng(random_state)
    centers = np.asarray(centers, dtype=float)
    counts = [n_samples // len(centers)] * len(centers)
    for index in range(n_samples - sum(counts)):
        counts[index] += 1

    features = []
    labels = []
    for label, (center, count) in enumerate(zip(centers, counts)):
        features.append(rng.normal(center, cluster_std, size=(count, centers.shape[1])))
        labels.append(np.full(count, label))

    X = np.vstack(features)
    y = np.concatenate(labels)
    order = rng.permutation(len(y))
    return X[order], y[order]


def make_regression(n_samples=200, n_features=3, noise=0.3, random_state=0):
    """Generate y = X @ coef + intercept + Gaussian noise with known coefficients."""
    rng = np.random.default_rng(random_state)
    X = rng.normal(size=(n_samples, n_features))
    true_coef = np.array([3.0, -2.0, 0.5])[:n_features]
    true_intercept = 1.5
    y = X @ true_coef + true_intercept + rng.normal(scale=noise, size=n_samples)
    return X, y, true_coef, true_intercept


def train_test_split(X, y, test_size=0.2):
    """Hold out the last fraction of an already shuffled dataset."""
    n_test = max(1, int(round(len(y) * test_size)))
    return X[:-n_test], X[-n_test:], y[:-n_test], y[-n_test:]


def main() -> int:
    print("=" * 66)
    print("ML from Scratch - one-command demo (NumPy only, no ML libraries)")
    print("=" * 66)

    # 1. k-NN: three overlapping Gaussian blobs -------------------------
    X, y = make_blobs(
        n_samples=600,
        centers=[[0.0, 0.0], [3.2, 0.4], [1.6, 2.8]],
        cluster_std=0.8,
        random_state=7,
    )
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    scaler = StandardScaler().fit(X_train)
    knn = KNN(n_neighbors=5).fit(scaler.transform(X_train), y_train)
    knn_accuracy = knn.score(scaler.transform(X_test), y_test)

    print(f"\n[1/3] k-NN | 3-class blobs | {len(X)} samples, {X.shape[1]} features")
    print(f"  model     : {knn!r}")
    print(f"  test score: accuracy = {knn_accuracy:.4f}")

    # 2. Linear regression: recover known coefficients -------------------
    X, y, true_coef, true_intercept = make_regression(
        n_samples=200, n_features=3, noise=0.3, random_state=11
    )
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    linear = LinearRegression().fit(X_train, y_train)
    linear_r2 = linear.score(X_test, y_test)
    linear_rmse = float(np.sqrt(mean_squared_error(y_test, linear.predict(X_test))))

    print(f"\n[2/3] LinearRegression | synthetic linear data | {len(X)} samples, {X.shape[1]} features")
    print(f"  model     : {linear!r}")
    print(f"  test score: R2 = {linear_r2:.4f}, RMSE = {linear_rmse:.4f}")
    print(
        f"  coef      : learned {np.array2string(linear.coef_, precision=3)}, "
        f"true {np.array2string(true_coef, precision=3)}"
    )
    print(f"  intercept : learned {linear.intercept_:.3f}, true {true_intercept:.3f}")

    # 3. Logistic regression: two overlapping Gaussian blobs -------------
    X, y = make_blobs(
        n_samples=500,
        centers=[[0.0, 0.0], [2.4, 2.4]],
        cluster_std=0.9,
        random_state=3,
    )
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    scaler = StandardScaler().fit(X_train)
    logistic = LogisticRegression(learning_rate=0.5, n_iters=1500).fit(
        scaler.transform(X_train), y_train
    )
    logistic_accuracy = logistic.score(scaler.transform(X_test), y_test)
    first_loss = logistic.loss_history_[0]
    final_loss = logistic.loss_history_[-1]

    print(f"\n[3/3] LogisticRegression | 2-class blobs | {len(X)} samples, {X.shape[1]} features")
    print(f"  model     : {logistic!r}")
    print(f"  test score: accuracy = {logistic_accuracy:.4f}")
    print(f"  train loss: {first_loss:.4f} -> {final_loss:.4f}")

    checks = [
        ("k-NN test accuracy >= 0.90", knn_accuracy >= 0.90),
        ("linear regression R2 >= 0.95", linear_r2 >= 0.95),
        (
            "linear regression recovers coefficients",
            float(np.max(np.abs(linear.coef_ - true_coef))) < 0.05
            and abs(linear.intercept_ - true_intercept) < 0.05,
        ),
        ("logistic regression test accuracy >= 0.88", logistic_accuracy >= 0.88),
        ("logistic regression loss decreased by half", final_loss <= 0.5 * first_loss),
    ]

    print("\n" + "-" * 66)
    for label, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    passed = sum(1 for _, ok in checks if ok)
    print(f"  {passed}/{len(checks)} checks passed")
    print("=" * 66)

    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
