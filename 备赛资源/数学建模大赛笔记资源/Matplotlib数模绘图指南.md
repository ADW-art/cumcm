# Matplotlib 数模绘图指南

## 一、基础配置

### 1.1 核心导入

```python
import matplotlib.pyplot as plt
import numpy as np
# plt 是 matplotlib 的绘图子库，所有绘图命令都通过它调用
```

### 1.2 中文显示（必须配置，否则中文变方块）

```python
plt.rcParams['font.sans-serif'] = ['SimHei']        # Windows 黑体
plt.rcParams['axes.unicode_minus'] = False           # 解决负号显示问题
```

备选字体（一个不行换下一个）：
| 系统 | 字体名 |
|------|--------|
| Windows | SimHei（黑体）, SimSun（宋体）, Microsoft YaHei（微软雅黑） |
| macOS | Arial Unicode MS, Heiti SC, PingFang SC |
| Linux | WenQuanYi Micro Hei, Source Han Sans CN |

### 1.3 全局风格设置

```python
plt.style.use('ggplot')                   # 仿 ggplot 风格，更美观
plt.rcParams['figure.figsize'] = (8, 5)   # 默认图大小（宽, 高）
plt.rcParams['figure.dpi'] = 150          # 分辨率
plt.rcParams['savefig.dpi'] = 300         # 保存时的分辨率
plt.rcParams['font.size'] = 12            # 全局字体大小
```

---

## 二、论文中最常用的 6 种图

### 2.1 折线图 —— 趋势与预测

用途：展示数据随时间或其他连续变量的变化趋势。预测类题目必用。

```python
x = np.array([1, 2, 3, 4, 5, 6, 7])
y1 = np.array([12, 15, 18, 20, 23, 25, 28])
y2 = np.array([10, 13, 16, 19, 21, 23, 26])  # 真实值

plt.plot(x, y1, 'ro-', label='预测值', linewidth=2, markersize=6)
plt.plot(x, y2, 'bs--', label='实际值', linewidth=2, markersize=6)
plt.xlabel('时间/天')
plt.ylabel('销售额/万元')
plt.title('销售额预测结果对比')
plt.legend()        # 显示图例
plt.grid(True, alpha=0.3)   # 半透明网格
plt.savefig('预测对比图.png', dpi=300, bbox_inches='tight')
plt.show()
```

**格式字符串说明**（如 'ro-'）：
| 字符 | 含义 | 常用值 |
|------|------|--------|
| 颜色 | r=红, b=蓝, g=绿, c=青, m=紫, y=黄, k=黑, w=白 |
| 标记 | o=圆点, s=方块, ^=三角, x=叉, \*=星号, D=菱形 |
| 线型 | -=实线, --=虚线, -=点划线, :=点线 |

组合示例：`'b^--'` = 蓝色三角虚线

### 2.2 柱状图/条形图 —— 对比与排序

用途：评价类题目的方案对比、多指标比较、数量级差异展示。

```python
类别 = ['方案A', '方案B', '方案C', '方案D']
得分 = [85, 92, 78, 88]

plt.bar(类别, 得分, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'], width=0.6)
plt.ylabel('综合得分')
plt.title('各方案综合评价结果')
# 在柱子上标数值
for i, v in enumerate(得分):
    plt.text(i, v + 1, str(v), ha='center', fontsize=11)
plt.savefig('柱状图.png', dpi=300, bbox_inches='tight')
plt.show()
```

分组柱状图（多指标对比）：
```python
x = np.arange(len(类别))
width = 0.35
plt.bar(x - width/2, [80, 90, 75, 85], width, label='指标1')
plt.bar(x + width/2, [88, 85, 82, 80], width, label='指标2')
plt.xticks(x, 类别)
plt.legend()
```

### 2.3 散点图 —— 分布与聚类

用途：K-Means 聚类结果展示、数据分布分析、相关性观察。

```python
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

X, _ = make_blobs(n_samples=200, centers=3, random_state=42)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)
centers = kmeans.cluster_centers_

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
for i in range(3):
    plt.scatter(X[labels==i, 0], X[labels==i, 1],
                c=colors[i], label=f'簇{i+1}', alpha=0.7, s=50)
plt.scatter(centers[:, 0], centers[:, 1],
            marker='x', c='black', s=200, linewidths=3, label='聚类中心')
plt.xlabel('特征1')
plt.ylabel('特征2')
plt.title('K-Means 聚类结果')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 2.4 热力图 —— 相关性矩阵与混淆矩阵

用途：特征相关性分析（做回归预测前必用）、分类模型评估。

```python
import pandas as pd

# 生成示例相关性矩阵
data = np.random.randn(100, 5)
df = pd.DataFrame(data, columns=['温度', '湿度', '风速', '降雨量', '销量'])
corr = df.corr()

plt.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
plt.colorbar(label='相关系数')
plt.xticks(range(5), corr.columns, rotation=30)
plt.yticks(range(5), corr.columns)
# 在每个格子里标数值
for i in range(5):
    for j in range(5):
        plt.text(j, i, f'{corr.iloc[i, j]:.2f}', ha='center', va='center',
                 fontsize=9, color='white' if abs(corr.iloc[i, j]) > 0.5 else 'black')
plt.title('特征相关性热力图')
plt.tight_layout()
plt.show()
```

### 2.5 直方图 —— 数据分布

用途：数据预处理环节，了解数据分布形态、检查异常值。

```python
data = np.random.randn(1000)  # 模拟正态分布数据
plt.hist(data, bins=30, color='#4ECDC4', edgecolor='white', alpha=0.7, density=True)
plt.xlabel('取值')
plt.ylabel('概率密度')
plt.title('数据分布直方图')
plt.grid(True, alpha=0.3)
plt.show()
```

### 2.6 子图 —— 多图组合在一张图中

用途：论文中节约版面，把多个相关图放在一起对比。

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

x = np.linspace(0, 10, 100)

axes[0, 0].plot(x, np.sin(x), 'r-')
axes[0, 0].set_title('sin(x)')
axes[0, 0].grid(True)

axes[0, 1].plot(x, np.cos(x), 'b--')
axes[0, 1].set_title('cos(x)')
axes[0, 1].grid(True)

axes[1, 0].plot(x, np.sin(x) + np.cos(x), 'g-.')
axes[1, 0].set_title('sin(x)+cos(x)')
axes[1, 0].grid(True)

axes[1, 1].plot(x, np.sin(x) * np.cos(x), 'm:')
axes[1, 1].set_title('sin(x)*cos(x)')
axes[1, 1].grid(True)

plt.tight_layout()
plt.show()
```

---

## 三、论文级图表美化

### 3.1 配色方案

论文图不要用默认配色（太刺眼）。推荐配色：

```python
# 科技期刊常用配色
colors = ['#3B7DD8', '#FF6B6B', '#4ECDC4', '#45B7D1',
          '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']

# 或者直接调用 colormap
colors = plt.cm.Set2(np.linspace(0, 1, 8))
```

### 3.2 图表规范设置（比赛时直接复制这段）

```python
# ===== 论文图表统一配置 =====
plt.rcParams.update({
    'font.size': 12,                     # 正文文字大小
    'axes.titlesize': 14,                # 标题大小
    'axes.labelsize': 12,                # 轴标签大小
    'xtick.labelsize': 11,               # X轴刻度大小
    'ytick.labelsize': 11,               # Y轴刻度大小
    'legend.fontsize': 11,               # 图例大小
    'figure.dpi': 150,                   # 显示分辨率
    'savefig.dpi': 300,                  # 保存分辨率
    'savefig.bbox': 'tight',             # 保存时自动裁剪空白
    'font.sans-serif': ['SimHei'],       # 中文字体
    'axes.unicode_minus': False,         # 负号正常显示
})
# =================================
```

### 3.3 保存图片的注意事项

```python
plt.savefig('图片名.png', dpi=300, bbox_inches='tight')
# bbox_inches='tight' 会自动裁剪多余的空白边距
# 论文中插图建议用 PNG 格式，不要用 JPG（会模糊）
```

图片放入 LaTeX 论文：
```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.7\textwidth]{图片名.png}
\caption{图片标题}  % 必须有标题，且在正文中被引用
\label{fig:example}
\end{figure}
如图~\ref{fig:example} 所示，...
```

---

## 四、实战场景：数模竞赛各环节的绘图安排

### 场景1：数据预处理阶段（比赛第1天）

| 图类型 | 用途 | 代码参考 |
|--------|------|---------|
| 直方图 | 检查各列数据分布 | plt.hist() |
| 箱线图 | 检测异常值 | plt.boxplot() |
| 热力图 | 特征相关性分析 | plt.imshow(corr) |

### 场景2：模型求解阶段（比赛第2天）

| 图类型 | 用途 | 代码参考 |
|--------|------|---------|
| 折线图 | 预测结果 vs 真实值 | plt.plot() |
| 散点图 | 聚类结果、拟合效果 | plt.scatter() |
| 柱状图 | 方案对比、指标对比 | plt.bar() |

### 场景3：结果分析阶段（比赛第3天）

| 图类型 | 用途 | 代码参考 |
|--------|------|---------|
| 折线图 | 灵敏度分析（参数变化对结果的影响） | plt.plot() |
| 子图 | 多组结果合并展示 | plt.subplots() |
| 柱状图 | 误差分析 | plt.bar() |

### 场景4：论文撰写阶段（比赛第3-4天）

```latex
论文中图的呈现方式：
- 每个图必须有 图号 + 标题（如"图1 预测结果对比"）
- 正文中必须引用每一张图（"如图X所示"）
- 统一配色、统一字体大小
- 保存为 PNG，分辨率 300dpi
```

---

## 五、常见问题排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 中文显示为方块 | 没配中文字体 | 加 rcParams 设 SimHei |
| 图太小/太大 | figure.figsize 没设 | plt.figure(figsize=(8,5)) |
| 坐标轴标签显示不全 | 汉字太长 | plt.tight_layout() |
| 图上中文乱码 | 字体不支持该字符 | 换字体（SimSun/微软雅黑） |
| 保存的图模糊 | dpi 太低 | savefig(dpi=300) |
| 图周围白边太多 | 没加 bbox_inches | savefig(bbox_inches='tight') |

---

## 六、一句话速查

```python
# 必记的 5 条命令（覆盖 80% 的需求）
plt.plot(x, y, '格式字符串')     # 折线图
plt.scatter(x, y)                # 散点图
plt.bar(x, height)               # 柱状图
plt.hist(data, bins=30)          # 直方图
plt.subplots(2, 2)               # 多子图

# 必记的 5 条设置
plt.xlabel('X轴')                # X轴标签
plt.ylabel('Y轴')                # Y轴标签
plt.title('标题')                # 图标题
plt.legend()                     # 图例
plt.grid(True, alpha=0.3)        # 网格线

# 保存为论文可用图片
plt.savefig('图.png', dpi=300, bbox_inches='tight')
```
