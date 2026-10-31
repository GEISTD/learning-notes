# ML from Scratch

用 NumPy 手写一组常见传统机器学习算法，重点是理解每个模型如何 `fit`、预测和评估。实现不调用 scikit-learn 或其他现成机器学习 estimator。

## 已实现算法

| 算法 | 任务 | 拟合/预测能力 |
|---|---|---|
| `LinearRegression` | 回归 | SVD 最小二乘，支持截距开关 |
| `LogisticRegression` | 二/多分类 | 全批量梯度下降、softmax、多类别概率、可选 L2 |
| `KNN` | 分类 | 欧氏距离、多数投票、类别概率 |
| `GaussianNB` | 分类 | 高斯特征似然、类别先验与概率 |
| `DecisionTreeClassifier` | 分类 | CART/Gini、深度和叶节点样本数限制 |
| `DecisionTreeRegressor` | 回归 | CART/平方误差分裂 |
| `RandomForestClassifier` | 分类 | bootstrap、随机特征、概率平均 |
| `RandomForestRegressor` | 回归 | bootstrap、随机特征、树预测平均 |
| `KMeans` | 聚类 | k-means++、多次初始化、惯性值与预测簇 |
| `PCA` | 降维 | SVD、方差解释率、正向和逆向变换 |

另有 `StandardScaler`、分类准确率、均方误差和 R²。除 PCA 变换器外，监督模型采用统一的 `fit(X, y) -> predict(X) -> score(X, y)` 接口；分类器提供 `predict_proba`。K-means 支持 `fit(X)`、`fit_predict(X)` 和 `predict(X)`。

## 安装和运行

只依赖 NumPy：

```bash
py -m pip install -r requirements.txt
py demo.py
py -m unittest discover -s tests -v
```

`demo.py` 会生成固定随机种子的分类、回归、聚类和降维样本，训练模型并检查结果。当前演示共 10 项检查，所有数据均本地生成，不需要联网或 sklearn。

## 快速示例

```python
from mlfs import LogisticRegression, StandardScaler

# 只用训练集拟合 scaler，避免把测试集信息泄漏进训练流程。
scaler = StandardScaler().fit(X_train)
model = LogisticRegression(learning_rate=0.2, n_iters=1500)
model.fit(scaler.transform(X_train), y_train)

predictions = model.predict(scaler.transform(X_test))
probabilities = model.predict_proba(scaler.transform(X_test))
print(model.score(scaler.transform(X_test), y_test))
```

其他模型同样通过构造函数设置超参数，再调用 `.fit(...)`。例如：

```python
from mlfs import KMeans, PCA, RandomForestClassifier

forest = RandomForestClassifier(n_estimators=50, max_depth=8, random_state=0)
forest.fit(X_train, y_train)

clusters = KMeans(n_clusters=3, random_state=0).fit_predict(X)
reduced = PCA(n_components=0.95).fit_transform(X)
```

## 实现说明

- 线性回归通过 `np.linalg.lstsq` 求解，避免显式求逆。
- 逻辑回归支持二分类 sigmoid 和多分类 softmax；`loss_history_` 可观察梯度下降过程。
- 决策树按特征阈值递归分裂；分类使用 Gini 不纯度，回归使用平方误差。
- 随机森林为每棵树抽取 bootstrap 样本，并在节点分裂时随机抽取特征。
- K-means 使用 k-means++ 初始化和多次重启；PCA 使用 SVD，不构造协方差矩阵再求逆。
- 训练属性以 `_` 结尾，超参数保留在普通属性中；模型随机性可由 `random_state` 复现。

## 目录

```text
ml-from-scratch/
├── demo.py
├── tests/test_estimators.py
└── mlfs/
    ├── base.py
    ├── cluster.py          # KMeans
    ├── decomposition.py    # PCA
    ├── ensemble.py         # RandomForest
    ├── knn.py
    ├── linear_regression.py
    ├── logistic_regression.py
    ├── metrics.py
    ├── naive_bayes.py      # GaussianNB
    ├── preprocessing.py
    └── tree.py             # 决策树分类/回归
```

这是面向学习的轻量实现，不承诺覆盖所有传统 ML 算法，也不替代经过优化的生产级库；例如 SVM、集成提升方法、特征缺失处理和稀疏矩阵目前不在范围内。
