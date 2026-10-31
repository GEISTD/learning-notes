import unittest

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
)


class EstimatorTests(unittest.TestCase):
    def setUp(self):
        self.X_class = np.array([[0.0], [0.1], [0.2], [2.8], [2.9], [3.0]])
        self.y_class = np.array(["cold"] * 3 + ["warm"] * 3)

    def test_classifiers_fit_predict_and_score(self):
        models = [
            KNN(n_neighbors=1),
            LogisticRegression(learning_rate=0.3, n_iters=1000),
            GaussianNB(),
            DecisionTreeClassifier(random_state=4),
            RandomForestClassifier(n_estimators=12, random_state=4),
        ]
        for model in models:
            with self.subTest(model=type(model).__name__):
                model.fit(self.X_class, self.y_class)
                np.testing.assert_array_equal(model.predict(self.X_class), self.y_class)
                self.assertEqual(model.score(self.X_class, self.y_class), 1.0)
                probabilities = model.predict_proba(self.X_class)
                self.assertEqual(probabilities.shape, (len(self.y_class), 2))
                np.testing.assert_allclose(probabilities.sum(axis=1), 1.0)

    def test_logistic_regression_multiclass(self):
        X = np.array([
            [-2.0, -1.0], [-1.8, -1.2], [-2.2, -0.8],
            [2.0, -1.0], [1.8, -1.2], [2.2, -0.8],
            [0.0, 2.0], [0.2, 1.8], [-0.2, 2.2],
        ])
        y = np.array(["left"] * 3 + ["right"] * 3 + ["top"] * 3)
        model = LogisticRegression(learning_rate=0.2, n_iters=1500).fit(X, y)
        self.assertGreaterEqual(model.score(X, y), 0.99)
        self.assertEqual(model.predict_proba(X).shape, (9, 3))
        self.assertLess(model.loss_history_[-1], model.loss_history_[0])

    def test_random_forest_multiclass_probabilities_align_classes(self):
        X = np.array([[-4.0], [-3.9], [0.0], [0.1], [4.0], [4.1]])
        y = np.array(["a", "a", "b", "b", "c", "c"])
        model = RandomForestClassifier(
            n_estimators=20, max_depth=3, random_state=21
        ).fit(X, y)
        probabilities = model.predict_proba(X)
        self.assertEqual(probabilities.shape, (len(y), 3))
        np.testing.assert_allclose(probabilities.sum(axis=1), 1.0)
        np.testing.assert_array_equal(model.predict(X), y)

    def test_regressors_fit_and_recover_values(self):
        X = np.arange(12, dtype=float).reshape(-1, 1)
        y = 2.5 * X[:, 0] - 4.0
        linear = LinearRegression().fit(X, y)
        np.testing.assert_allclose(linear.predict(X), y, atol=1e-10)
        self.assertAlmostEqual(linear.score(X, y), 1.0)

        tree = DecisionTreeRegressor(max_depth=3, random_state=2).fit(X, y)
        self.assertEqual(tree.predict(X).shape, y.shape)
        self.assertGreater(tree.score(X, y), 0.9)

        forest = RandomForestRegressor(
            n_estimators=20, max_depth=4, random_state=2
        ).fit(X, y)
        self.assertEqual(forest.predict(X).shape, y.shape)
        self.assertGreater(forest.score(X, y), 0.9)

    def test_kmeans_fit_predict_and_score(self):
        X = np.array([
            [-5.0, -5.0], [-5.1, -4.9], [-4.9, -5.1],
            [5.0, 5.0], [5.1, 4.9], [4.9, 5.1],
        ])
        model = KMeans(n_clusters=2, n_init=4, random_state=3).fit(X)
        np.testing.assert_array_equal(model.predict(X), model.labels_)
        self.assertLess(model.inertia_, 0.1)
        self.assertAlmostEqual(model.score(X), -model.inertia_)
        np.testing.assert_array_equal(
            KMeans(n_clusters=2, n_init=4, random_state=3).fit_predict(X),
            model.labels_,
        )

    def test_pca_transform_and_inverse(self):
        X = np.array([
            [1.0, 2.0, 3.0], [2.0, 4.0, 6.0],
            [3.0, 6.0, 9.0], [4.0, 8.0, 12.0],
        ])
        pca = PCA(n_components=1)
        reduced = pca.fit_transform(X)
        self.assertEqual(reduced.shape, (4, 1))
        np.testing.assert_allclose(pca.inverse_transform(reduced), X, atol=1e-10)
        self.assertAlmostEqual(float(pca.explained_variance_ratio_.sum()), 1.0)

        by_variance = PCA(n_components=0.99).fit(X)
        self.assertEqual(by_variance.n_components_, 1)
        self.assertEqual(PCA(n_components=1.0).fit(X).n_components_, 1)

    def test_validation_errors_are_clear(self):
        with self.assertRaises(RuntimeError):
            DecisionTreeClassifier().predict(self.X_class)
        with self.assertRaises(ValueError):
            KMeans(n_clusters=7).fit(self.X_class)
        with self.assertRaises(ValueError):
            PCA(n_components=0).fit(self.X_class)
        with self.assertRaises(ValueError):
            GaussianNB().fit(self.X_class, np.zeros(len(self.y_class)))


if __name__ == "__main__":
    unittest.main()
