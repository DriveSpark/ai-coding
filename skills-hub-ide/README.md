# AI Skills Hub Manager

这是一个用于管理和分发 AI Agent Skills 的工具套件。它可以帮助你轻松地将本地开发的 Skills 源码库同步到多个 AI IDE 环境中（如 Trae, Antigravity 等）。

## 🚀 推荐方式：Agent Skills Manager (Python)

这是我们最新推出的**跨平台、全功能**管理工具，具备交互式菜单、智能环境检测和强大的错误引导功能。

### 安装与使用

该工具本身就是一个标准的 Skill，你可以直接将其作为 Skill 安装到你的 Agent 中使用，或者直接运行源码：

```bash
# 进入工具目录
cd skills-hub-ide/agent-skills-manager

# 运行安装命令 (支持批量扫描)
python3 scripts/main.py install /path/to/your/skills_source
```

### 核心特性

- **跨平台支持**: 完美运行于 MacOS, Linux 和 Windows。
- **交互式菜单**: 使用方向键 (`↑`/`↓`) 和空格键轻松选择目标 IDE。
- **批量处理**: 自动扫描目录下所有的 Skills 并批量安装。
- **智能纠错**: 遇到权限问题 (Errno 1) 会自动生成一键修复命令。
- **两阶段分发**: 采用 `Source -> Hub -> IDE` 架构，确保一次更新，多处同步。

---

## 📂 旧版工具 (Legacy)

如果你无法使用 Python 环境，可以使用针对特定系统的 Shell 脚本。

### 1. MacOS / Linux (Bash)

**运行分发管理器**：

```bash
cd skills-hub-ide/MacOS
./skills_manager.sh
```

**操作流程：**

1.  **输入源路径**：拖入 Skills 文件夹。
2.  **自动同步**：同步到 `~/.agents/skills`。
3.  **选择目标**：使用方向键选择 IDE。

### 2. Windows (PowerShell)

**运行分发管理器**：

进入 `skills-hub-ide\Windows` 目录，直接双击运行 `skills_manager.bat`。

---

## 文件结构

- `agent-skills-manager/`: **[推荐]** Python 版核心工具（跨平台）
  - `scripts/main.py`: 主程序入口
  - `scripts/core/`: 核心逻辑库
- `MacOS/`: [旧版] Bash 脚本
- `Windows/`: [旧版] PowerShell 脚本
- `README.md`: 本说明文档

## 注意事项

- **软链接机制**：本工具使用软链接 (`ln -s` 或 Windows Symlink) 实现同步。
- **权限提示**：在受限环境（如 IDE 内置终端）中如果遇到权限错误，请根据工具提示复制命令到外部终端运行。

---

Generated for AI Skills Workflow
