# LaTeX 语法速查笔记（基于竞赛论文模板）

## 一、文档基础结构

### 1. 文档类声明（模板第1行）
```latex
\documentclass[12pt,a4paper]{article}
```
- `[12pt]`：正文字号
- `[a4paper]`：纸张大小
- `{article}`：文档类型（论文用 article）

### 2. 导言区 vs 正文区
```
\documentclass{...}    ← 导言区开始
\usepackage{...}        ← 导入宏包
\begin{document}        ← 正文开始
  ...你的内容...
\end{document}          ← 正文结束
```

**导言区**：放宏包、设置命令。**正文区**：放实际内容。

### 3. 编译方式
```powershell
xelatex 文件名.tex
```
本模板需要 xelatex 编译，因为它使用中文支持包 ctex。

---

## 二、中文支持（模板第4-7行）

```latex
\usepackage{ctex}       % 中文支持（核心）
\usepackage{fontspec}   % 字体设置
\setmainfont{Times New Roman}  % 英文字体设为 Times New Roman
```

- **必须用 xelatex 编译**，不能用 pdflatex
- `ctex` 会自动处理中文换行、字体等问题
- 中文和英文混排时，英文自动用 Times New Roman

---

## 三、数学公式（模板第9-10行）

### 1. 行内公式
```latex
$c_i$           % 单个变量
$\alpha$        % 希腊字母
$\sum_{i=1}^n$  % 求和符号
$[-20\%, +20\%]$  % 带百分号的范围
```

### 2. 行间公式（带编号）
```latex
\begin{equation}
  \label{eq:model1}
  \min Z = \sum_{i=1}^{n} c_i x_i
\end{equation}
```
- 自动生成编号 (1), (2), ...
- `\label{eq:model1}` 设标签，`\ref{eq:model1}` 引用编号

### 3. 多行公式对齐
```latex
\begin{align}
  \text{s.t.} \quad & \sum_{i=1}^{n} a_{ij} x_i \leq b_j,\quad j=1,\dots,m \\
  & x_i \geq 0,\quad i=1,\dots,n
\end{align}
```
- `&` 标记对齐位置
- `\\` 换行
- `\quad` 插入空格
- `\text{s.t.}` 在公式中插入文字
- `\dots` 省略号

### 4. 模板中的公式命令速查

| 命令 | 效果 | 说明 |
|------|------|------|
| `$x_1$` | $x_1$ | 下标 |
| `$\alpha$` | $\alpha$ | 希腊字母α |
| `$\beta$` | $\beta$ | 希腊字母β |
| `$\varepsilon$` | $\varepsilon$ | 希腊字母ε |
| `\sum_{i=1}^{n}` | $\sum_{i=1}^{n}$ | 求和 |
| `\min` | $\min$ | 最小值 |
| `\leq` | $\leq$ | 小于等于 |
| `\geq` | $\geq$ | 大于等于 |
| `\times` | $\times$ | 乘号 |
| `\cdots` | $\cdots$ | 水平省略号 |

---

## 四、页面设置（模板第13-16行）

```latex
\usepackage{geometry}
\geometry{left=2.5cm, right=2.5cm, top=2.5cm, bottom=2.5cm}
```

按官方格式规范：上下左右页边距至少2.5厘米。

---

## 五、图表（模板第18-23行）

### 1. 插入表格
```latex
\begin{table}[H]
\centering
\caption{表格标题}
\label{tab:result1}
\begin{tabular}{cccc}      % 4列，居中
  \toprule                  % 顶部粗线（booktabs宏包提供）
  列1 & 列2 & 列3 & 列4 \\
  \midrule                  % 中间细线
  数据 & & & \\
  \bottomrule               % 底部粗线
\end{tabular}
\end{table}
```

**表格参数说明：**
- `{cccc}`：4列居中。`l`=左对齐，`c`=居中，`r`=右对齐，`|`=竖线
- `[H]`：**强制表格放在当前位置**（需要float宏包）
- `\toprule`、`\midrule`、`\bottomrule`：三线表风格（需要booktabs宏包）
- `\caption{}`：图表标题
- `\label{}`：标签，配合`\ref{}`在文中引用

### 2. 插入图片
```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.7\textwidth]{figure1.png}
\caption{结果可视化图}
\label{fig:result1}
\end{figure}
```

**引用表格或图片：**
```latex
如表~\ref{tab:result1}所示...
从图~\ref{fig:result1}可以看出...
```

---

## 六、枚举列表（模板第73-90行）

### 1. 有序列表（编号）
```latex
\begin{enumerate}
  \item 假设一：...
  \item 假设二：...
\end{enumerate}
```

### 2. 无序列表（圆点）
```latex
\begin{itemize}
  \item 模型结构清晰...
  \item ...
\end{itemize}
```

---

## 七、代码块（模板第28-47行）

```latex
\usepackage{listings}     % 代码展示
\usepackage{xcolor}       % 代码语法高亮颜色
```

在正文中插入代码：
```latex
\begin{lstlisting}[caption=代码标题]
% 你的代码
for i = 1:10
    disp(i);
end
\end{lstlisting}
```

**模板中预设的代码样式：**
- 语言：Python（也可改成MATLAB等）
- 自动行号，左侧显示
- 关键字蓝色、注释绿色、字符串红色
- 自动换行

如果放的是MATLAB代码，改成：
```latex
\lstset{language=MATLAB}   % 或放在\begin{lstlisting}[language=MATLAB]
```

---

## 八、页眉页脚（模板第39-46行）

```latex
\usepackage{fancyhdr}
\pagestyle{fancy}
\setlength{\headheight}{14.5pt}              % 页眉高度（已修复warning）
\lhead{山西大学第二十届数学建模竞赛}          % 页眉左
\chead{}                                      % 页眉中
\rhead{\thepage}                              % 页眉右（页码）
\renewcommand{\headrulewidth}{0.4pt}          % 页眉横线粗细
```

注意：`\thepage` 是当前页码。按官方要求，页码从摘要页开始（用阿拉伯数字从1开始）。

---

## 九、标题设置（模板第49-52行）

```latex
\usepackage{titlesec}
\titleformat{\section}{\Large\bfseries}{}{0em}{}
\titleformat{\subsection}{\large\bfseries}{}{0em}{}
```

正文中写章节：
```latex
\section{问题重述}           % 一级标题
\subsection{问题背景}        % 二级标题
```

---

## 十、引用与参考文献（模板最后）

### 1. 文中引用
```latex
如表~\ref{tab:result1}所示...      % 引用表格编号
从图~\ref{fig:result1}可以看出...   % 引用图片编号
由公式~\ref{eq:model1}可得...       % 引用公式编号
```

### 2. 参考文献列表
```latex
\begin{thebibliography}{9}
  \bibitem{ref1} 作者. 论文题目[J]. 期刊名, 年份, 卷(期): 起止页码.
  \bibitem{ref2} 作者. 书名[M]. 出版地: 出版社, 出版年份.
\end{thebibliography}
```

文中引用某个文献：
```latex
如文献~\cite{ref1}所述...
```

**参考文献类型标识：**
| 标识 | 文献类型 |
|------|---------|
| [J] | 期刊论文 |
| [M] | 专著/教材 |
| [D] | 学位论文 |
| [R] | 报告 |
| [C] | 会议论文 |
| [S] | 标准 |
| [P] | 专利 |
| [EB/OL] | 电子资源 |

---

## 十一、封面页（模板第55-75行）

```latex
\begin{titlepage}        % 开始封面页
\centering               % 内容居中
\vspace*{3cm}            % 垂直空3cm
{\Huge\bfseries 标题}    % 超大号加粗文字
\\[2cm]                  % 换行+空2cm
\vfill                   % 撑满剩余空间
\begin{tabular}{rl}      % 表格：2列（右对齐+左对齐）
  参赛队员1： & 姓名1 \\
\end{tabular}
\end{titlepage}
```

**字号命令对照表：**
| 命令 | 对应字号 |
|------|---------|
| `\tiny` | 最小 |
| `\small` | 小 |
| `\normalsize` | 正常 |
| `\large` | 大 |
| `\Large` | 更大 |
| `\LARGE` | 很大 |
| `\huge` | 巨大 |
| `\Huge` | 最大 |

**字体修饰：**
| 命令 | 效果 |
|------|------|
| `\textbf{文字}` | **加粗** |
| `\textit{文字}` | *斜体* |
| `\underline{文字}` | 下划线 |
| `\texttt{文字}` | 等宽字体（代码风格）|

---

## 十二、摘要页写法

```latex
\begin{center}
  {\LARGE\bfseries 摘要}
\end{center}
\begin{quotation}
  \noindent
  本文针对...
\end{quotation}
\vspace{0.5cm}
\noindent\textbf{关键词：} 关键词一；关键词二
```

- `\begin{quotation}`：缩进引用环境，用于摘要正文
- `\noindent`：取消段首缩进
- `\vspace{0.5cm}`：垂直空0.5厘米

---

## 十三、附录

```latex
\appendix              % 声明进入附录模式（编号变为A, B, C...）
\section{附录：核心代码}
\begin{lstlisting}[caption=主程序文件]
  ...
\end{lstlisting}
```

---

## 十四、常用符号速查（带模板示例）

### 希腊字母
| 命令 | 显示 | 命令 | 显示 |
|------|------|------|------|
| `\alpha` | α | `\beta` | β |
| `\gamma` | γ | `\delta` | δ |
| `\varepsilon` | ε | `\theta` | θ |
| `\mu` | μ | `\sigma` | σ |
| `\omega` | ω | `\pi` | π |

### 数学运算
| 命令 | 显示 | 用途 |
|------|------|------|
| `\frac{a}{b}` | a/b | 分数 |
| `\sqrt{x}` | √x | 开方 |
| `\sum_{i=1}^n` | ∑ | 求和 |
| `\prod_{i=1}^n` | ∏ | 连乘 |
| `\int_a^b` | ∫ | 积分 |
| `\partial` | ∂ | 偏微分 |
| `\lim_{x\to0}` | lim | 极限 |

### 括号
| 命令 | 显示 |
|------|------|
| `\{ \}` | {}（需要转义） |
| `\left( \right)` | 自动调整大小的括号 |
| `\left[ \right]` | 自动调整大小的方括号 |
| `\lVert \rVert` | 范数符号 |

### 箭头
| 命令 | 显示 |
|------|------|
| `\to` | → |
| `\rightarrow` | → |
| `\Rightarrow` | ⇒ |
| `\leftarrow` | ← |
| `\Leftarrow` | ⇐ |
| `\longrightarrow` | ⟶ |

### 集合
| 命令 | 显示 |
|------|------|
| `\in` | ∈ |
| `\notin` | ∉ |
| `\subset` | ⊂ |
| `\subseteq` | ⊆ |
| `\cup` | ∪ |
| `\cap` | ∩ |
| `\emptyset` | ∅ |

---

## 十五、完整编译流程

```powershell
# 第一次编译（生成.aux辅助文件）
xelatex 竞赛论文模板.tex

# 第二次编译（稳定交叉引用）
xelatex 竞赛论文模板.tex
```

**为什么编译两次？**
第一次生成标签引用关系（.aux文件），第二次才能正确显示 `\ref{}` 和 `\cite{}` 的编号。
如果引用的编号显示为"??"，说明需要再次编译。

**如果改动了参考文献：**
```powershell
xelatex 竞赛论文模板.tex
bibtex  竞赛论文模板              % 处理参考文献
xelatex 竞赛论文模板.tex
xelatex 竞赛论文模板.tex
```

---

## 十六、常见报错及解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `! Undefined control sequence` | 命令打错了 | 检查拼写 |
| `! Missing $ inserted` | 数学命令没在公式模式 | 给公式加$...$ |
| `! Extra }` | 括号不匹配 | 检查{}配对 |
| `! File not found` | 图片找不到 | 确认图片路径和文件名 |
| `! Package ctex Error` | 没用xelatex | 改用xelatex编译 |
| `Reference ... undefined` | 标签没定义 | 检查\label拼写 |
| 编译乱码 | 文件编码问题 | 保存为UTF-8编码 |

---

## 十七、模板的论文结构回顾

本模板按官方格式规范组织论文如下：

1. **封面页** - 标题、题号、队员、指导教师、日期
2. **摘要页** - 摘要正文 + 关键词（**电子版论文的第一页**）
3. **正文开始** - 从第4页起
   - 问题重述
   - 模型假设与符号说明
   - 模型的建立与求解（核心，含公式+代码+图表）
   - 结果分析与检验（灵敏度分析+误差分析）
   - 模型评价与改进
4. **参考文献**
5. **附录** - 核心代码

**官方格式要点：**
- 摘要不超过一页
- 正文不超过30页
- 电子版论文不要放承诺书和编号专用页
- 不要目录
- 页边距至少2.5cm
- 引用他人成果必须标注
