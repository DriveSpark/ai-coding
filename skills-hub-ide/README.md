# AI Skills Hub Manager

这是一个用于管理和分发 AI Agent Skills 的命令行工具套件。它可以帮助你轻松地将本地开发的 Skills 源码库同步到多个 AI IDE 环境中（如 Trae, Antigravity 等）。

## 核心功能

1.  **Skills Manager**: 交互式主程序，负责将源码分发到各个 IDE。
    - MacOS/Linux: `MacOS/skills_manager.sh`
    - Windows: `Windows/skills_manager.bat`
2.  **Symlink Tool**: 底层核心工具，负责创建软链接，支持命令行参数调用。
    - MacOS/Linux: `MacOS/link.sh`
    - Windows: `Windows/link.ps1`

## 快速开始

### MacOS / Linux

1.  **运行分发管理器**
    这是最常用的方式，通过交互式菜单一键同步。

    ```bash
    cd skills-hub-ide/MacOS
    ./skills_manager.sh
    ```

    **操作流程：**
    1.  **输入源路径**：脚本会提示你输入 Skills 的源码文件夹路径（支持直接把文件夹拖入终端）。
    2.  **自动同步**：脚本会自动将源码同步到系统中间层 (`~/.agents/skills`)。
    3.  **选择目标 IDE**：
        - 使用 `↑` / `↓` 移动光标
        - 使用 `空格键` 选中或取消目标 IDE (Trae / Antigravity)
        - 按 `Enter` 确认执行
        - 按 `ESC` 或 `q` 退出

2.  **单独使用链接工具**
    如果你需要自定义链接任务，可以直接使用底层工具：

    ```bash
    cd skills-hub-ide/MacOS
    # 查看帮助
    ./link.sh --help

    # 示例：将我的技能库链接到 Trae
    ./link.sh -s /Users/me/my-skills -t ~/.trae/skills -y
    ```

### Windows

1.  **运行分发管理器**

    进入 `skills-hub-ide\Windows` 目录，直接双击运行 `skills_manager.bat`。

    或者在 PowerShell 中运行：

    ```powershell
    cd skills-hub-ide\Windows
    .\skills_manager.ps1
    ```

2.  **单独使用链接工具**

    ```powershell
    cd skills-hub-ide\Windows
    # 查看帮助
    .\link.ps1 -Help

    # 示例
    .\link.ps1 -Source C:\my-skills -Target C:\Users\Me\.trae\skills
    ```

## 文件结构

- `MacOS/`: MacOS 和 Linux 系统的脚本
  - `skills_manager.sh`: 交互式主程序
  - `link.sh`: 核心逻辑（软链接生成器）
- `Windows/`: Windows 系统的脚本
  - `skills_manager.bat`: 交互式主程序启动入口
  - `skills_manager.ps1`: 交互式主程序逻辑
  - `link.ps1`: 核心逻辑（PowerShell 版）
- `README.md`: 本说明文档

## 注意事项

- **软链接机制**：本工具使用软链接 (`ln -s` 或 Windows Symlink) 实现同步。这意味着你只需要维护一份源码，IDE 里看到的永远是最新版本，无需反复复制粘贴。
- **同名跳过**：如果目标目录已经存在同名文件或文件夹，脚本会自动跳过，**不会覆盖**现有内容，确保安全。
- **Windows 权限**：在 Windows 上创建符号链接可能需要管理员权限（取决于系统设置），如果遇到权限错误，请尝试以管理员身份运行终端。

---

Generated for AI Skills Workflow
