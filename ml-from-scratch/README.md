# ML from Scratch

Three classic machine learning models implemented from scratch with NumPy, sharing one
minimal scikit-learn-style interface. No ML libraries, no dataset downloads — cloning the
repository and running one command is enough.

## Models

| Model | Task | Learning method | Default metric |
| --- | --- | --- | --- |
| `KNN` | Classification | Euclidean distance + majority vote | Accuracy |
| `LinearRegression` | Regression | Ordinary least squares (SVD) | R² |
| `LogisticRegression` | Binary classification | Full-batch gradient descent | Accuracy |

Every model is still a few dozen lines of readable code; NumPy is used only for array math,
not for ready-made estimators.

## Quickstart

```bash
pip install -r requirements.txt
python demo.py
```

On Windows, use `py demo.py` if `python` is not on your `PATH`.

That single command generates the datasets, trains all three models, evaluates them on a
held-out test set, and runs sanity checks. Example output:

```text
==================================================================
ML from Scratch - one-command demo (NumPy only, no ML libraries)
==================================================================

[1/3] k-NN | 3-class blobs | 600 samples, 2 features
  model     : KNN(n_neighbors=5)
  test score: accuracy = 0.9667

[2/3] LinearRegression | synthetic linear data | 200 samples, 3 features
  model     : LinearRegression(fit_intercept=True)
  test score: R2 = 0.9906, RMSE = 0.3378
  coef      : learned [ 2.997 -1.992  0.491], true [ 3.  -2.   0.5]
  intercept : learned 1.517, true 1.500

[3/3] LogisticRegression | 2-class blobs | 500 samples, 2 features
  model     : LogisticRegression(learning_rate=0.5, n_iters=1500, l2=0.0)
  test score: accuracy = 0.9800
  train loss: 0.6931 -> 0.0912

------------------------------------------------------------------
  [PASS] k-NN test accuracy >= 0.90
  [PASS] linear regression R2 >= 0.95
  [PASS] linear regression recovers coefficients
  [PASS] logistic regression test accuracy >= 0.88
  [PASS] logistic regression loss decreased by half
  5/5 checks passed
==================================================================
```

The exit code is non-zero if any check fails, so `demo.py` doubles as a smoke test.

## Unified API

All estimators follow the same lifecycle: `fit` → `predict` → `score` (plus `predict_proba`
for the classifier that supports it). Fitted attributes end with `_`, hyperparameters do not.

```python
import numpy as np

from mlfs import KNN, LinearRegression, LogisticRegression, StandardScaler

X_train, X_test, y_train, y_test = ...

scaler = StandardScaler().fit(X_train)

model = KNN(n_neighbors=5).fit(scaler.transform(X_train), y_train)
predictions = model.predict(scaler.transform(X_test))
accuracy = model.score(scaler.transform(X_test), y_test)

print(model)          # KNN(n_neighbors=5)
print(model.get_params())  # {'n_neighbors': 5}
```

Swapping models requires no other changes — only the constructor differs:

```python
LinearRegression(fit_intercept=True)
LogisticRegression(learning_rate=0.5, n_iters=1500, l2=0.0)
```

`StandardScaler` is also written from scratch and, importantly, is fitted on the training
split only to avoid data leakage.

## Project layout

```text
ml-from-scratch/
├── demo.py                    # one-command runner + sanity checks
├── requirements.txt
└── mlfs/
    ├── __init__.py
    ├── base.py                # BaseEstimator, classifier/regressor mixins, input checks
    ├── metrics.py             # accuracy, MSE, R²
    ├── preprocessing.py       # StandardScaler
    ├── knn.py
    ├── linear_regression.py
    └── logistic_regression.py
```

## Implementation notes

- **k-NN** computes all pairwise squared distances with the
  `|a|² + |b|² - 2ab` expansion, then uses `argsort` for the nearest neighbours and
  `bincount` for the vote. Ties are broken towards the smallest class label.
- **Linear regression** builds a design matrix with a leading column of ones and solves it
  with `np.linalg.lstsq`, i.e. SVD-based least squares rather than a normal-equation inverse.
- **Logistic regression** minimizes binary cross-entropy with optional L2 regularization
  using full-batch gradient descent. `loss_history_` records the loss after every iteration.
- **Datasets** are generated deterministically inside `demo.py` with NumPy, so the demo needs
  no network access and results are reproducible. Scikit-learn is intentionally not a
  dependency — not even for its bundled toy datasets.

## Results

With the fixed seeds used in `demo.py`:

| Model | Dataset | Test score |
| --- | --- | --- |
| `KNN(k=5)` | 600 samples, 3 classes, 2 features | 0.9667 accuracy |
| `LinearRegression()` | 200 samples, 3 features, known coefficients | 0.9906 R² |
| `LogisticRegression()` | 500 samples, 2 classes, 2 features | 0.9800 accuracy |

Exact values may vary slightly across NumPy/BLAS versions, but the sanity thresholds are
loose enough to stay stable.

## Requirements

- Python 3.9+
- NumPy 1.24+
