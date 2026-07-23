"""
============================================
竞赛工具库 —— 数据预处理/灵敏度分析/可视化
============================================
用法: from 竞赛工具库 import *
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ===== 1. matplotlib 全局样式 =====
# 放在代码最前面，所有图表风格统一
def set_plot_style():
    """一键设置论文级图表样式"""
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    rcParams['axes.unicode_minus'] = False  # 正常显示负号
    rcParams['figure.figsize'] = (8, 5)
    rcParams['figure.dpi'] = 150
    rcParams['savefig.dpi'] = 300
    rcParams['savefig.bbox'] = 'tight'
    rcParams['font.size'] = 12
    rcParams['axes.titlesize'] = 14
    rcParams['axes.labelsize'] = 12
    rcParams['legend.fontsize'] = 10
    rcParams['xtick.labelsize'] = 10
    rcParams['ytick.labelsize'] = 10
    rcParams['lines.linewidth'] = 2
    rcParams['lines.markersize'] = 6
    rcParams['grid.alpha'] = 0.3
    print("[OK] 图表样式已应用 (字体: 微软雅黑, DPI: 300)")


# ===== 2. 数据预处理 =====
def explore_data(df):
    """快速查看数据概况"""
    print("【数据概况】")
    print(f"  行数: {df.shape[0]}, 列数: {df.shape[1]}")
    print(f"  缺失值总数: {df.isnull().sum().sum()}")
    print(f"  重复行数: {df.duplicated().sum()}")
    print("\n【各列信息】")
    info = pd.DataFrame({
        '类型': df.dtypes,
        '非空数': df.count(),
        '缺失数': df.isnull().sum(),
        '缺失率': (df.isnull().sum() / len(df)).round(4),
        '唯一值': df.nunique(),
    })
    print(info.to_string())
    return info

def handle_missing(df, strategy='auto'):
    """智能处理缺失值"""
    df = df.copy()
    for col in df.columns:
        null_count = df[col].isnull().sum()
        if null_count == 0:
            continue
        if strategy == 'auto':
            if df[col].dtype in ['float64', 'int64']:
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else '')
        elif strategy == 'drop':
            df = df.dropna(subset=[col])
        elif strategy == 'median':
            df[col] = df[col].fillna(df[col].median())
        elif strategy == 'mean':
            df[col] = df[col].fillna(df[col].mean())
    return df

def detect_outliers(df, method='iqr', threshold=1.5):
    """检测异常值"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers = {}
    for col in numeric_cols:
        if method == 'iqr':
            Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower, upper = Q1 - threshold * IQR, Q3 + threshold * IQR
            mask = (df[col] < lower) | (df[col] > upper)
        elif method == 'zscore':
            z = np.abs((df[col] - df[col].mean()) / df[col].std())
            mask = z > threshold
        outliers[col] = {'个数': mask.sum(), '占比': f"{mask.mean()*100:.1f}%"}
    return pd.DataFrame(outliers).T

def normalize(df, method='minmax'):
    """标准化/归一化"""
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if method == 'minmax':
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min() + 1e-10)
        elif method == 'zscore':
            df[col] = (df[col] - df[col].mean()) / (df[col].std() + 1e-10)
        elif method == 'robust':
            median, iqr = df[col].median(), df[col].quantile(0.75) - df[col].quantile(0.25)
            df[col] = (df[col] - median) / (iqr + 1e-10)
    return df


# ===== 3. 模型评价指标 =====
def regression_metrics(y_true, y_pred):
    """回归模型评价指标"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mse = np.mean((y_true - y_pred) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(y_true - y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100
    r2 = 1 - np.sum((y_true - y_pred) ** 2) / (np.sum((y_true - y_true.mean()) ** 2) + 1e-10)
    return {'MSE': round(mse, 4), 'RMSE': round(rmse, 4),
            'MAE': round(mae, 4), 'MAPE(%)': round(mape, 2),
            'R²': round(r2, 4)}

def classification_metrics(y_true, y_pred):
    """分类模型评价指标"""
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return {
        '准确率': round(accuracy_score(y_true, y_pred), 4),
        '精确率': round(precision_score(y_true, y_pred, average='weighted', zero_division=0), 4),
        '召回率': round(recall_score(y_true, y_pred, average='weighted', zero_division=0), 4),
        'F1分数': round(f1_score(y_true, y_pred, average='weighted', zero_division=0), 4),
    }


# ===== 4. 灵敏度分析 =====
def sensitivity_analysis(model_func, param_name, base_value, param_range, fixed_params=None):
    """单参数灵敏度分析
    model_func: 模型函数，接收参数值返回结果
    param_name: 参数名
    base_value: 基准值
    param_range: 参数变化范围，如 np.linspace(-0.2, 0.2, 9) 表示 -20% 到 +20%
    fixed_params: 固定参数字典
    """
    results = []
    for change in param_range:
        param_val = base_value * (1 + change)
        params = {param_name: param_val}
        if fixed_params:
            params.update(fixed_params)
        result = model_func(**params)
        results.append({'变化率': f"{change*100:+.0f}%", '参数值': round(param_val, 4),
                        '结果': round(result, 4)})
    return pd.DataFrame(results)

def plot_sensitivity(df_result, ylabel='目标值', title='灵敏度分析'):
    """绘制灵敏度分析图"""
    set_plot_style()
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    # 折线图
    ax[0].plot(range(len(df_result)), df_result['结果'], 'bo-', linewidth=2)
    ax[0].set_xticks(range(len(df_result)))
    ax[0].set_xticklabels(df_result['变化率'])
    ax[0].set_xlabel('参数变化率')
    ax[0].set_ylabel(ylabel)
    ax[0].set_title(title)
    ax[0].grid(True, alpha=0.3)
    # 柱状图 - 偏差
    base = df_result['结果'].iloc[len(df_result)//2]
    changes = (df_result['结果'] - base) / base * 100
    colors = ['red' if c < 0 else 'green' for c in changes]
    ax[1].bar(range(len(df_result)), changes, color=colors, alpha=0.7)
    ax[1].axhline(y=0, color='black', linewidth=0.5)
    ax[1].set_xticks(range(len(df_result)))
    ax[1].set_xticklabels(df_result['变化率'])
    ax[1].set_xlabel('参数变化率')
    ax[1].set_ylabel('结果变化率(%)')
    ax[1].set_title('参数-结果变化关系')
    ax[1].grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


# ===== 5. 结果 → LaTeX 表格导出 =====
def df_to_latex(df, caption='', label='', precision=4):
    """DataFrame 转 LaTeX 三线表"""
    latex = df.round(precision).to_latex(
        index=True,
        caption=caption,
        label=label,
        escape=False,
        column_format='l' + 'c' * (len(df.columns)),
    )
    # 替换默认表格线为三线表
    latex = latex.replace('\\hline', '')
    latex = latex.replace('\\begin{tabular}', '\\begin{tabular}\n\\toprule')
    lines = latex.split('\n')
    result = []
    for i, line in enumerate(lines):
        if '\\midrule' in line or '\\toprule' in line:
            result.append(line)
            continue
        if i == 2:  # 表头后加 midrule
            result.append('\\midrule')
        if i == len(lines) - 3:  # 最后一行前加 bottomrule
            result.append('\\bottomrule')
        result.append(line)
    return '\n'.join(result)


# ===== 6. 快速绘图模板 =====
def quick_plot(x, y, xlabel='', ylabel='', title='', kind='line',
               labels=None, save_path=None):
    """快速绘图模板"""
    set_plot_style()
    fig, ax = plt.subplots(figsize=(8, 5))
    if kind == 'line':
        if labels:
            for i, (yi, label) in enumerate(zip(y, labels)):
                ax.plot(x, yi, 'o-', linewidth=2, label=label, markersize=4)
        else:
            ax.plot(x, y, 'o-', linewidth=2, markersize=4)
    elif kind == 'bar':
        ax.bar(x, y, alpha=0.7, edgecolor='black', linewidth=0.5)
    elif kind == 'scatter':
        ax.scatter(x, y, alpha=0.6, edgecolors='black', linewidth=0.5)
    elif kind == 'hist':
        ax.hist(y if y is not None else x, bins=20, alpha=0.7, edgecolor='black')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    if labels:
        ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] 已保存: {save_path}")
    return fig, ax


# ===== 7. 模型结果对比表 =====
def compare_models(models_results):
    """整合多个模型的评价指标做对比"""
    df = pd.DataFrame(models_results).T
    df['排名'] = df.iloc[:, 0].rank(ascending=False).astype(int)
    df = df.sort_values('排名')
    return df
