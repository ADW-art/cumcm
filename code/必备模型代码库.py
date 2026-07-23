# ============================================
# 数学建模竞赛 —— 必备模型代码库（Python版）
# 每个模型都包含：函数定义 + 使用示例
# 库依赖: numpy, scipy, pandas, matplotlib, sklearn
# ============================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import linprog, minimize, curve_fit
from scipy.stats import zscore
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import warnings
warnings.filterwarnings('ignore')

# ==============================
# 1. 层次分析法（AHP）
#   适用：评价类问题，指标难以量化，数据量少
# ==============================
def ahp(judgment_matrix):
    """
    层次分析法：计算权重向量和一致性比例
    judgment_matrix: 判断矩阵 (n x n)
    返回: (权重向量, 一致性比例)
    """
    n = len(judgment_matrix)
    # 计算特征向量（几何平均法）
    product = np.prod(judgment_matrix, axis=1)
    weight = product ** (1/n)
    weight = weight / weight.sum()
    # 计算最大特征值
    aw = judgment_matrix @ weight
    lambda_max = (aw / weight).mean()
    # 计算一致性指标CI
    CI = (lambda_max - n) / (n - 1)
    # 随机一致性指标RI（1-10阶）
    RI_table = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12,
                6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    RI = RI_table.get(n, 1.49)
    CR = CI / RI if RI > 0 else 0  #一致性比例--<=0.1就合理
    return weight, CR

# 使用示例
def ahp_example():
    print("=" * 50)
    print("示例1：层次分析法（AHP）")
    print("=" * 50)
    # 4个准则对目标的判断矩阵
    matrix = np.array([
        [1,   1/3, 1/2, 1/4],
        [3,   1,   2,   1/2],
        [2,   1/2, 1,   1/3],
        [4,   2,   3,   1  ]
    ])
    weight, CR = ahp(matrix)
    print(f"权重向量: {np.round(weight, 4)}")
    print(f"一致性比例CR: {CR:.4f}")
    if CR < 0.1:
        print("CR < 0.1，判断矩阵一致性可接受")
    else:
        print("CR >= 0.1，需要调整判断矩阵")
    print()


# ==============================
# 2. TOPSIS法（优劣解距离法）
# ==============================
def topsis(data, weights, positive_indicator=True):
    """
    TOPSIS综合评价法
    data: 决策矩阵 (m个方案 x n个指标)
    weights: 各指标权重
    positive_indicator: 各指标是否为正向指标(越大越好)，默认全是
    返回: 各方案的得分(接近程度)
    """
    m, n = data.shape
    # 正向化处理
    if isinstance(positive_indicator, bool):
        positive_indicator = [positive_indicator] * n
    data_pos = data.copy()
    for i in range(n):
        if not positive_indicator[i]:
            data_pos[:, i] = 1 / data[:, i]  # 逆向转正向
    # 标准化
    norm = np.sqrt((data_pos ** 2).sum(axis=0))
    norm_data = data_pos / norm
    # 加权
    weighted = norm_data * weights
    # 正负理想解
    z_plus = weighted.max(axis=0)
    z_minus = weighted.min(axis=0)
    # 计算距离
    d_plus = np.sqrt(((weighted - z_plus) ** 2).sum(axis=1))
    d_minus = np.sqrt(((weighted - z_minus) ** 2).sum(axis=1))
    # 计算得分
    score = d_minus / (d_plus + d_minus)
    return score

def topsis_example():
    print("=" * 50)
    print("示例2：TOPSIS综合评价法")
    print("=" * 50)
    # 5个城市的4项指标
    data = np.array([
        [88, 75, 1.2, 3000],   # 城市A
        [92, 82, 1.5, 3500],   # 城市B
        [78, 90, 0.8, 2800],   # 城市C
        [85, 70, 1.0, 3200],   # 城市D
        [90, 85, 1.1, 3100],   # 城市E
    ])
    weights = np.array([0.3, 0.3, 0.2, 0.2])
    # 假设第2个指标是越小越好（逆向）
    scores = topsis(data, weights,
                    positive_indicator=[True, True, True, True])
    for i, s in enumerate(scores):
        print(f"方案{i+1}的综合评分为: {s:.4f}")
    print(f"最优方案: 方案{scores.argmax()+1}")
    print()


# ==============================
# 3. 灰色预测模型 GM(1,1)
# ==============================
def gm11(data, n_pred=5):
    """
    灰色预测 GM(1,1) 模型
    data: 原始数据序列
    n_pred: 预测步数
    返回: (拟合值, 预测值)
    """
    n = len(data)
    # 累加生成
    x1 = np.cumsum(data)
    # 构造B矩阵和Y向量
    B = np.zeros((n-1, 2))
    Y = np.zeros((n-1, 1))
    for i in range(n-1):
        B[i, 0] = -0.5 * (x1[i] + x1[i+1])
        B[i, 1] = 1
        Y[i, 0] = data[i+1]
    # 最小二乘法求参数
    params = np.linalg.inv(B.T @ B) @ B.T @ Y
    a, b = params[0, 0], params[1, 0]
    # 预测
    pred = np.zeros(n + n_pred)
    for k in range(n + n_pred):
        pred[k] = (data[0] - b/a) * (1 - np.exp(a)) * np.exp(-a * k)
    return pred[:n], pred[n:]

def gm11_example():
    print("=" * 50)
    print("示例3：灰色预测模型 GM(1,1)")
    print("=" * 50)
    # 某城市近5年GDP数据
    data = np.array([12.3, 13.5, 14.8, 16.2, 17.9])
    fit, pred = gm11(data, n_pred=3)
    for i in range(len(data)):
        print(f"年份{i+1}: 实际={data[i]:.1f}, 拟合={fit[i]:.1f}")
    for i in range(len(pred)):
        print(f"预测第{len(data)+i+1}年: {pred[i]:.1f}")
    print()


# ==============================
# 4. 线性规划
# ==============================
def linear_programming_example():
    print("=" * 50)
    print("示例4：线性规划")
    print("=" * 50)
    # 例：max Z = 3x1 + 2x2
    #     s.t. 2x1 + x2 <= 10
    #          x1 + x2 <= 8
    #          x1, x2 >= 0
    # scipy默认求min，取负转换为min
    c = [-3, -2]  # 目标函数系数（求min）
    A = [[2, 1], [1, 1]]  # 约束矩阵
    b = [10, 8]  # 约束右端项
    bounds = [(0, None), (0, None)]  # x1, x2 >= 0
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    if res.success:
        print(f"最优解: x1={res.x[0]:.2f}, x2={res.x[1]:.2f}")
        print(f"最优目标值: {-res.fun:.2f}")
    else:
        print("求解失败:", res.message)
    print()


# ==============================
# 5. 多元线性回归
# ==============================
def linear_regression_example():
    print("=" * 50)
    print("示例5：多元线性回归")
    print("=" * 50)
    # 生成模拟数据：Y = 2 + 3X1 - 1.5X2 + noise
    np.random.seed(42)
    X = np.random.randn(100, 2)
    y = 2 + 3 * X[:, 0] - 1.5 * X[:, 1] + np.random.randn(100) * 0.5
    model = LinearRegression()
    model.fit(X, y)
    print(f"截距: {model.intercept_:.4f}")
    print(f"系数: {model.coef_}")
    print(f"R-sq: {model.score(X, y):.4f}")
    y_pred = model.predict(X)
    rmse = np.sqrt(np.mean((y - y_pred)**2))
    print(f"RMSE: {rmse:.4f}")
    print()


# ==============================
# 6. K-Means聚类
# ==============================
def kmeans_example():
    print("=" * 50)
    print("示例6：K-Means聚类分析")
    print("=" * 50)
    np.random.seed(42)
    # 生成3簇数据
    X = np.vstack([
        np.random.randn(50, 2) + [2, 2],
        np.random.randn(50, 2) + [-2, 2],
        np.random.randn(50, 2) + [0, -2]
    ])
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    centers = kmeans.cluster_centers_
    print(f"聚类中心:\n{centers}")
    # 统计每个类别的样本数
    unique, counts = np.unique(labels, return_counts=True)
    for u, c in zip(unique, counts):
        print(f"类别{u}: {c}个样本")
    # 可视化
    plt.figure(figsize=(8, 6))
    colors = ['red', 'blue', 'green']
    for i in range(3):
        plt.scatter(X[labels==i, 0], X[labels==i, 1],
                    c=colors[i], label=f'簇{i+1}', alpha=0.6)
    plt.scatter(centers[:, 0], centers[:, 1],
                marker='x', c='black', s=200, linewidths=3, label='聚类中心')
    plt.title('K-Means聚类结果')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(r'E:\code\数学建模大赛\备赛资源\代码\kmeans_demo.png', dpi=100)
    plt.close()
    print("聚类图已保存")
    print()


# ==============================
# 7. 逻辑回归（二分类）
# ==============================
def logistic_regression_example():
    print("=" * 50)
    print("示例7：逻辑回归（二分类）")
    print("=" * 50)
    np.random.seed(42)
    X = np.random.randn(200, 3)
    y = (X[:, 0] + X[:, 1] - X[:, 2] > 0).astype(int)
    model = LogisticRegression()
    model.fit(X, y)
    print(f"训练准确率: {model.score(X, y):.2%}")
    print(f"模型系数: {model.coef_[0]}")
    print()


# ==============================
# 8. BP神经网络（预测）
# ==============================
def bpnn_example():
    print("=" * 50)
    print("示例8：BP神经网络预测")
    print("=" * 50)
    np.random.seed(42)
    X = np.random.randn(200, 5)
    y = np.sin(X[:, 0]) + np.cos(X[:, 1]) + 0.5 * X[:, 2]
    split = 160
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    # 标准化
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    mlp = MLPRegressor(hidden_layer_sizes=(10, 5),
                        max_iter=500, random_state=42)
    mlp.fit(X_train_scaled, y_train)
    y_pred = mlp.predict(X_test_scaled)
    mse = np.mean((y_test - y_pred)**2)
    print(f"测试集MSE: {mse:.4f}")
    print(f"R-sq: {mlp.score(X_test_scaled, y_test):.4f}")
    print()


# ==============================
# 9. SIR传染病模型（微分方程）
# ==============================
def sir_model(beta, gamma, S0, I0, R0, days):
    """
    SIR传染病模型（欧拉法）
    beta: 感染率
    gamma: 恢复率
    S0, I0, R0: 初始易感、感染、恢复人数
    days: 模拟天数
    返回: (S, I, R)时间序列
    """
    N = S0 + I0 + R0
    S, I, R = [S0], [I0], [R0]
    for _ in range(days):
        dS = -beta * S[-1] * I[-1] / N
        dI = beta * S[-1] * I[-1] / N - gamma * I[-1]
        dR = gamma * I[-1]
        S.append(S[-1] + dS)
        I.append(I[-1] + dI)
        R.append(R[-1] + dR)
    return np.array(S), np.array(I), np.array(R)

def sir_example():
    print("=" * 50)
    print("示例9：SIR传染病模型")
    print("=" * 50)
    beta, gamma = 0.3, 0.1
    S0, I0, R0 = 990, 10, 0
    days = 100
    S, I, R = sir_model(beta, gamma, S0, I0, R0, days)
    plt.figure(figsize=(10, 6))
    t = np.arange(days + 1)
    plt.plot(t, S, 'b-', label='易感者 S', linewidth=2)
    plt.plot(t, I, 'r-', label='感染者 I', linewidth=2)
    plt.plot(t, R, 'g-', label='恢复者 R', linewidth=2)
    plt.xlabel('时间/天')
    plt.ylabel('人数')
    plt.title('SIR传染病模型模拟')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(r'E:\code\数学建模大赛\备赛资源\代码\sir_demo.png', dpi=100)
    plt.close()
    print(f"感染峰值: {I.max():.0f}人 (第{I.argmax()}天)")
    print(f"最终感染人数: {R[-1]:.0f}人")
    print("SIR模型图已保存")
    print()


# ==============================
# 10. 熵权法（客观赋权）
# ==============================
def entropy_weight(data):
    """
    熵权法计算客观权重
    data: 决策矩阵 (m个方案 x n个指标)
    返回: 各指标的熵权
    """
    # 归一化
    norm_data = data / data.sum(axis=0)
    # 计算熵值
    e = -np.sum(norm_data * np.log(norm_data + 1e-10), axis=0) / np.log(len(data))
    # 计算权重
    w = (1 - e) / (1 - e).sum()
    return w

def entropy_example():
    print("=" * 50)
    print("示例10：熵权法")
    print("=" * 50)
    data = np.array([
        [85, 92, 78, 88],
        [90, 88, 82, 85],
        [78, 95, 80, 90],
        [92, 80, 85, 82],
    ])
    weights = entropy_weight(data)
    print(f"各指标权重: {np.round(weights, 4)}")
    print()


# ==============================
# 主程序：运行所有示例
# ==============================
if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  数学建模竞赛必备模型代码库")
    print("  使用说明：单独导入每个函数即可使用")
    print("=" * 60 + "\n")
    
    ahp_example()
    topsis_example()
    gm11_example()
    linear_programming_example()
    linear_regression_example()
    kmeans_example()
    logistic_regression_example()
    bpnn_example()
    sir_example()
    entropy_example()
    
    print("所有模型示例运行完成！")
    print(f"说明：以上代码需要以下Python包：")
    print("  pip install numpy scipy pandas matplotlib scikit-learn")
