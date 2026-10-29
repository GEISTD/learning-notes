# 手写三个机器学习模型（只用 NumPy）

用 sklearn 的时候 `fit` 一行就出结果，但不知道里面在算什么。所以把三个最基础的模型各手写一遍，接口做成 sklearn 的样子，方便互相替换。

## 三个模型

| 模型 | 任务 | 方法 | 指标 |
|---|---|---|---|
| `KNN` | 分类 | 欧氏距离 + 多数投票 | 准确率 |
| `LinearRegression` | 回归 | 最小二乘（SVD 解） | R² |
| `LogisticRegression` | 二分类 | 全批量梯度下降 | 准确率 |

每个模型几十行，NumPy 只用来做数组运算，没有调用现成的 estimator。

## 跑法

```bash
pip install -r requirements.txt
python demo.py        # Windows 上 python 不在 PATH 就用 py demo.py
```

`demo.py` 会生成数据、训练三个模型、在测试集上打分，最后跑五项断言：

```text
[1/3] k-NN | 3-class blobs | 600 samples, 2 features
  test score: accuracy = 0.9667
[2/3] LinearRegression | 200 samples, 3 features
  test score: R2 = 0.9906, RMSE = 0.3378
  coef: learned [ 2.997 -1.992  0.491], true [ 3.  -2.   0.5]
[3/3] LogisticRegression | 500 samples, 2 classes
  test score: accuracy = 0.9800
  train loss: 0.6931 -> 0.0912
5/5 checks passed
```

任何一项不过，退出码非 0，所以它同时当冒烟测试用。

## 接口

统一是 `fit` → `predict` → `score`，分类器另有 `predict_proba`。学到的属性带下划线结尾，超参数不带——这条是跟 sklearn 学的，换模型时只改构造函数：

```python
from mlfs import KNN, LinearRegression, LogisticRegression, StandardScaler

scaler = StandardScaler().fit(X_train)          # 只在训练集上 fit
model = KNN(n_neighbors=5).fit(scaler.transform(X_train), y_train)
print(model.score(scaler.transform(X_test), y_test))
print(model.get_params())                        # {'n_neighbors': 5}
```

## 几个实现上的选择

- **KNN** 用 `|a|² + |b|² - 2ab` 展开算全部样本对的距离，比双重循环快；`argsort` 取前 k 个，`bincount` 投票，票数相同取标签小的那个。
- **线性回归** 用 `np.linalg.lstsq`，不写 `(XᵀX)⁻¹Xᵀy`——直接求逆在特征共线时数值不稳。
- **逻辑回归** 用二元交叉熵，可选 L2，全批量梯度下降；`loss_history_` 存每次迭代的 loss，方便看收敛。
- **数据** 在 `demo.py` 里用固定种子生成，不联网、不依赖 sklearn 自带数据集，结果可复现。
- **标准化** 只在训练集上 fit，再 transform 测试集，避免数据泄漏。

## 结果

固定种子下：

| 模型 | 数据 | 测试集 |
|---|---|---|
| `KNN(k=5)` | 600 样本，3 类，2 特征 | 0.9667 |
| `LinearRegression()` | 200 样本，3 特征，已知系数 | R² 0.9906 |
| `LogisticRegression()` | 500 样本，2 类，2 特征 | 0.9800 |

不同 NumPy/BLAS 版本小数位会有差异，断言的阈值留得比较宽。

## 目录

```text
ml-from-scratch/
├── demo.py
├── requirements.txt
└── mlfs/
    ├── base.py              BaseEstimator、输入检查
    ├── metrics.py           accuracy / MSE / R²
    ├── preprocessing.py     StandardScaler
    ├── knn.py
    ├── linear_regression.py
    └── logistic_regression.py
```

## 还没做

- 逻辑回归目前只有二分类，多分类要再加 softmax 或 one-vs-rest
- 梯度下降是全批量的，样本量上去以后要换 mini-batch
- 想加一组和 sklearn 的数值对比测试，确认手写实现的结果能对上
