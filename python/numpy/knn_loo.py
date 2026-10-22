"""Handwritten k-NN with per-fold min-max normalization and leave-one-out CV."""

from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris


def min_max_normalize(train_x: np.ndarray, test_x: np.ndarray):
    """Normalize using only the training fold; constant columns map to zero."""
    minimum = np.min(train_x, axis=0)
    feature_range = np.max(train_x, axis=0) - minimum
    safe_range = np.where(feature_range == 0, 1.0, feature_range)
    normalized_train = (train_x - minimum) / safe_range
    normalized_test = (test_x - minimum) / safe_range
    return normalized_train, normalized_test


def predict_one(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray, k: int):
    """Predict one label using Euclidean distance and a handwritten majority vote."""
    # Euclidean distance, computed directly with NumPy (no distance/KNN library).
    differences = train_x - test_x
    distances = np.sqrt(np.sum(differences * differences, axis=1))
    nearest_indices = np.argsort(distances, kind="stable")[:k]
    nearest_labels = train_y[nearest_indices]

    # Counter preserves first-seen order, so ties go to the closest tied label.
    votes = Counter(nearest_labels.tolist())
    return max(votes, key=votes.get)


def leave_one_out_accuracy(features: np.ndarray, labels: np.ndarray, k: int) -> float:
    """Return LOO accuracy, fitting normalization separately inside each fold."""
    correct = 0
    sample_count = len(labels)

    for held_out in range(sample_count):
        train_mask = np.ones(sample_count, dtype=bool)
        train_mask[held_out] = False
        train_x = features[train_mask]
        train_y = labels[train_mask]
        test_x = features[held_out]

        normalized_train, normalized_test = min_max_normalize(train_x, test_x)
        prediction = predict_one(normalized_train, train_y, normalized_test, k)
        correct += prediction == labels[held_out]

    return correct / sample_count


def main():
    # Iris is used only as a sample dataset; the classifier and normalization
    # are implemented above rather than delegated to scikit-learn.
    iris = load_iris()
    features = iris.data.astype(float)
    labels = iris.target

    ks = np.arange(1, 16)
    accuracies = [leave_one_out_accuracy(features, labels, int(k)) for k in ks]

    for k, accuracy in zip(ks, accuracies):
        print(f"k={k:2d}  LOO accuracy={accuracy:.4f}")

    best_index = int(np.argmax(accuracies))
    print(f"Best k={ks[best_index]} (accuracy={accuracies[best_index]:.4f})")

    plt.figure(figsize=(8, 5))
    plt.plot(ks, accuracies, marker="o")
    plt.xticks(ks)
    plt.ylim(0, 1.05)
    plt.xlabel("k")
    plt.ylabel("LOO accuracy")
    plt.title("Handwritten k-NN: Leave-One-Out Accuracy")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("knn_loo_accuracy.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()
