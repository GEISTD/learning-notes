# 逻辑回归从零推导：NumPy 实现 + 手推全过程

> S1 阶段学习笔记 · 2026-10-14
> 覆盖：NumPy 最小集、sigmoid、BCE 损失（MLE 推导）、梯度手推（dL/dz = a−y）、predict 与评估指标、数值梯度验证

---

## 1. NumPy 最小必备集

```python
import numpy as np

# 数据形状约定：X 是 (样本数 n, 特征数 m)，y 是 (n, 1) 列向量
X = np.array([[0.5, 1.2], [1.5, -0.3], [2.2, 0.1]])   # 3 个样本，2 个特征
y = np.array([[1], [0], [1]])                          # 标签，统一 (n,1) 防广播坑

w = np.zeros((2, 1))   # 权重 (m,1)，初始全 0
b = 0.0
z = X @ w + b          # 矩阵乘法 → (3,1)；标量 b 自动广播到每个样本

np.exp(z)                          # 逐元素 e^z
np.log(z)                          # 逐元素 ln z（z 必须 > 0）
np.clip(z, 1e-12, 1 - 1e-12)       # 夹在区间内 —— 防 log(0)
np.mean(z); np.sum(z, axis=0)      # 平均 / 按列求和
X.T                                # 转置 (n,m) → (m,n)
```

### 唯一的经典坑：(n,) vs (n,1)

`(n,)` 和 `(n,1)` 相加会广播成 `(n,n)` 矩阵——全错但**不报错**。从数据加载那一刻就统一：

```python
y = y.reshape(-1, 1)
```

### 同族函数

```python
np.ones((2, 1))      # 全 1
np.full((2, 1), 7)   # 全填 7
np.zeros_like(w)     # 照抄 w 的形状建全 0 数组（写 num_grad 时用，最稳）
```

---

## 2. sigmoid：把任意实数压成概率

$$\sigma(z) = \frac{1}{1+e^{-z}}$$

| z | a = σ(z) |
|---|---|
| → +∞ | → 1 |
| 0 | 0.5 |
| → −∞ | → 0 |

导数的漂亮性质（后面推梯度全靠它）：

$$\sigma'(z) = \sigma(z)\,(1-\sigma(z)) = a(1-a)$$

实现：

```python
def sigmoid(z):
    return 1 / (1 + np.exp(-z))
```

---

## 3. BCE 损失：从 MLE（极大似然）推导

### 第 1 步：单个样本的概率（伯努利分布）

二分类 y ∈ {0, 1}，模型预测 a = σ(z) 是“y=1 的概率”。一行通吃两种情况：

$$P(y|x) = a^{y}(1-a)^{1-y}$$

验证：y=1 时只剩 $a^1(1-a)^0 = a$ ✓；y=0 时 $a^0(1-a)^1 = 1-a$ ✓

### 第 2 步：n 个独立样本的似然

独立 → 联合概率 = 连乘：

$$L(w,b) = \prod_{i=1}^{n} a_i^{y_i}(1-a_i)^{1-y_i}$$

MLE 目标：找 w, b 让“观测到的数据”出现概率最大。

### 第 3 步：取对数（连乘变连加，防数值下溢）

$$\ln L = \sum_{i=1}^{n} \left[ y_i \ln a_i + (1-y_i)\ln(1-a_i) \right]$$

### 第 4 步：最大化 → 最小化（加负号取平均）

$$\boxed{\text{BCE} = -\frac{1}{n}\sum_{i=1}^{n}\left[ y_i \ln a_i + (1-y_i)\ln(1-a_i) \right]}$$

直观含义：真实 y=1 时预测 a 越接近 1 损失越小；真实 y=0 时 a 越接近 0 损失越小；完全预测反 → 损失冲向无穷大。

实现：

```python
def bce(y, a, eps=1e-12):
    a = np.clip(a, eps, 1 - eps)          # 防 log(0)
    return -np.mean(y * np.log(a) + (1 - y) * np.log(1 - a))
```

---

## 4. 梯度推导：dL/dz = a − y

对单个样本，链式法则拆两段：

$$\frac{\partial L}{\partial z} = \frac{\partial L}{\partial a} \cdot \frac{\partial a}{\partial z}$$

**第一段**（对 ln a 求导是 1/a）：

$$\frac{\partial L}{\partial a} = -\frac{y}{a} + \frac{1-y}{1-a} = \frac{a-y}{a(1-a)}$$

**第二段**（sigmoid 导数）：

$$\frac{\partial a}{\partial z} = a(1-a)$$

**相乘，分母恰好消掉**：

$$\frac{\partial L}{\partial z} = \frac{a-y}{a(1-a)} \cdot a(1-a) = \boxed{a - y}$$

结论：**梯度 = 预测 − 真实**。预测对了梯度趋近 0，错得越狠梯度越大（与线性回归 MSE 的推导一脉相承）。

### 向量化到 w 和 b

z = Xw + b，所以 ∂z/∂w = X、∂z/∂b = 1。n 个样本取平均：

$$dw = \frac{1}{n} X^{T}(a-y), \qquad db = \frac{1}{n}\sum_{i=1}^{n}(a_i - y_i)$$

维度验证：X 是 (n,m)，(a−y) 是 (n,1)，$X^T(a-y)$ → (m,1)，与 w 形状一致——这就是要转置的原因。

实现（每个一行）：

```python
a  = sigmoid(X @ w + b)          # (n,1)
dw = X.T @ (a - y) / n           # (m,1)
db = np.sum(a - y) / n           # 标量
w -= lr * dw
b -= lr * db                     # 梯度下降一步
```

---

## 5. predict 与评估指标

```python
pred = (a >= 0.5).astype(int)               # 概率 → 0/1 决策
# 混淆矩阵四个数，纯布尔运算（pred 和 y 都是 (n,1) 的 int）
TP = int(np.sum((pred == 1) & (y == 1)))    # 真正例：预测1，实际1
TN = int(np.sum((pred == 0) & (y == 0)))
FP = int(np.sum((pred == 1) & (y == 0)))    # 假正例：误报
FN = int(np.sum((pred == 0) & (y == 1)))    # 假负例：漏报

acc  = (TP + TN) / n
prec = TP / (TP + FP + 1e-12)   # "我说患病的人里，真患病的比例"
rec  = TP / (TP + FN + 1e-12)   # "真患病的人里，被我抓出的比例"
```

---

## 6. 数值梯度：验证手推的杀手锏

不用等别人检查——用差分近似验证你推的 dw 对不对：

```python
def num_grad(f, w, eps=1e-5):
    g = np.zeros_like(w)
    for i in range(len(w)):
        wp, wm = w.copy(), w.copy()
        wp[i] += eps
        wm[i] -= eps
        g[i] = (f(wp) - f(wm)) / (2 * eps)
    return g

# 若 num_grad 求出的 ≈ 手推的 dw，推导就是对的
```

---

## 7. 训练循环骨架

```python
w = np.zeros((X.shape[1], 1))
b = 0.0
lr = 0.1

for epoch in range(500):
    a = sigmoid(X @ w + b)
    loss = bce(y, a)
    dw = X.T @ (a - y) / n
    db = np.sum(a - y) / n
    w -= lr * dw
    b -= lr * db
    if epoch % 100 == 0:
        print(f"epoch {epoch}: loss = {loss:.4f}")
```

loss 稳定下降 = 实现正确。不下降先查：学习率、形状广播、梯度公式。

---

## 动手清单（核心代码必须手写）

- [ ] 写 `sigmoid(z)`，测试 σ(0)=0.5、σ(±20) 不溢出
- [ ] 写 `bce(y, a)`，测试：完美预测损失≈0，全错预测损失巨大
- [ ] **纸上手推 dL/dz = a−y**（第 4 节两段链式），然后写 `gradients()`
- [ ] 用 `num_grad` 数值验证手推的 dw
- [ ] 训练 500 轮看 loss 下降 → predict → 混淆矩阵四格 + acc/prec/rec
