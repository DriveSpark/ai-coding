# Agent Skill Manager (Python)

跨平台的 AI 技能管理工具。使用 Python 编写，旨在提供一致的跨平台体验。

## 目录结构

```
skills-hub-py/
├── main.py              # CLI 入口
└── core/                # 核心模块
    ├── config.py        # 路径配置
    ├── detector.py      # IDE 探测器
    ├── linker.py        # 跨平台链接器
    └── utils.py         # 工具函数
```

## 核心功能

1.  **自动中转站管理**: 自动维护 `~/.agents/skills` 目录。
2.  **IDE 自动探测**: 智能扫描 Trae、Antigravity 等 IDE 的安装位置。
3.  **两级分发**: 实现 `源码 -> 中转站 -> IDE` 的自动链路创建。

## 用法

确保你已经安装了 Python 3。

```bash
# 1. 安装一个 Skill (自动分发到所有探测到的 IDE)
python3 main.py install /path/to/your/local/skill
```

## 支持的 IDE

目前支持自动探测以下 IDE：
- Trae (`~/.trae/skills`)
- Antigravity (`~/.gemini/antigravity/skills`)
