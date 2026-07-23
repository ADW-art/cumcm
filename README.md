# CUMCM 数学建模竞赛备赛资源库

> 山西大学第二十届数学建模竞赛 | 2026年8月10日 — 8月13日

## 📂 目录结构

```
E:\code\数学建模大赛\
├── code/                    ← Python代码库（模型实现 + 工具函数）
│   ├── 必备模型代码库.py    10个常用模型的Python实现
│   ├── 竞赛工具库.py        数据预处理/可视化/灵敏度分析工具
│   └── my_topsis_tutorial.py  TOPSIS手把手教程
│
├── 备赛资源/
│   ├── 模板/                 LaTeX论文模板
│   ├── 代码/                 MATLAB模型代码库 + 示例图
│   ├── 历届赛题/             2024/2016/2015年CUMCM真题
│   ├── 数学建模大赛笔记资源/  笔记/规范/模型速查/LaTeX语法
│   ├── 竞赛计时器.html        74小时倒计时器
│   └── 每日学习清单.md        备赛每日计划
│
└── README.md
```

## 🚀 快速开始

### Python环境
```powershell
# 激活虚拟环境
E:\code\数学建模大赛\.venv\Scripts\Activate.ps1

# 运行模型代码库验证环境
python code\必备模型代码库.py
```

### LaTeX编译论文
```powershell
xelatex "备赛资源\模板\竞赛论文模板.tex"
```

## 🤝 协作说明

### 如何向本仓库推送文件

1. **安装Git**（如未安装）：https://git-scm.com/downloads
2. **配置GitHub认证**（选一种方式）：

   **方式A：GitHub CLI（推荐）**
   ```powershell
   winget install --id GitHub.cli
   gh auth login
   ```

   **方式B：Git Credential Manager**
   ```powershell
   git credential-manager github login
   ```

   **方式C：Personal Access Token**
   - 在 https://github.com/settings/tokens 创建token
   - 推送时用token作为密码

3. **克隆仓库**
   ```powershell
   git clone https://github.com/ADW-art/cumcm.git
   ```

4. **添加并推送文件**
   ```powershell
   git add .
   git commit -m "添加了xxx"
   git push
   ```

### ⚠️ 注意事项
- 大文件（>100MB）已被 .gitignore 排除，不会上传
- .venv 虚拟环境不要提交
- 建议每次推送前先 `git pull` 拉取最新版本

## 📚 资源说明

| 资源 | 来源 | 说明 |
|------|------|------|
| 论文格式规范PDF | mcm.edu.cn | 2026年修订稿，官方正本 |
| 参赛规则PDF | mcm.edu.cn | 2026年修订稿，官方正本 |
| 2024年CUMCM赛题 | cumcm.icourses.cn | A/B/C/D/E五题+完整附件 |
| LaTeX模板 | 自编 | 符合官方格式要求 |
| Python代码库 | 自编 | 10个模型 + 工具函数库 |

## 📅 竞赛关键时间

- **校赛**: 2026年8月10日 18:00 — 8月13日 20:00
- **提交邮箱**: sxushuxuejianmo@163.com
- **QQ群**: 1054471630
