# Agent Skill Manager (Python) Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个跨平台（Windows/MacOS/Linux）的 Agent Skill Manager，使用 Python 实现，具备两级自动分发架构（源码 -> 中转站 -> IDE），并最终封装为标准 Skill。

**Architecture:**

- **Language**: Python 3 (使用标准库，零依赖)
- **Structure**: CLI 入口 + 核心逻辑模块 (Linker, Detector, Config)
- **Flow**: 自动探测本机 IDE -> 建立中转站链接 -> 建立 IDE 链接

**Tech Stack:** Python 3 (`pathlib`, `os`, `sys`, `argparse`)

---

### Task 1: 基础设施搭建

**Files:**

- Create: `skills-hub-ide/skills-hub-py/main.py`
- Create: `skills-hub-ide/skills-hub-py/core/__init__.py`
- Create: `skills-hub-ide/skills-hub-py/core/config.py`
- Create: `skills-hub-ide/skills-hub-py/core/utils.py`

**Step 1: 创建目录结构**

```bash
mkdir -p skills-hub-ide/skills-hub-py/core
touch skills-hub-ide/skills-hub-py/core/__init__.py
```

**Step 2: 编写 `config.py`**

定义全局常量和路径配置。

```python
import os
import sys
from pathlib import Path

# 获取用户主目录
HOME = Path.home()

# 中转站路径: ~/.agents/skills
AGENTS_HUB = HOME / ".agents" / "skills"

# 常见 IDE 的 Skills 目录候选列表
# 格式: (IDE名称, 相对HOME的路径)
IDE_CANDIDATES = [
    ("Trae", ".trae/skills"),
    ("Antigravity", ".gemini/antigravity/skills"),
    # 未来可扩展 VSCode 等
]

def get_platform():
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('darwin'):
        return 'macos'
    else:
        return 'linux'
```

**Step 3: 编写 `utils.py` (日志与辅助)**

```python
import sys

def log_info(msg):
    print(f"[\033[92mINFO\033[0m] {msg}")

def log_warn(msg):
    print(f"[\033[93mWARN\033[0m] {msg}")

def log_error(msg):
    print(f"[\033[91mERROR\033[0m] {msg}")
    sys.exit(1)
```

**Step 4: Commit**

```bash
git add skills-hub-ide/skills-hub-py
git commit -m "feat: init python project structure and config"
```

---

### Task 2: 核心探测器 (Detector)

**Files:**

- Create: `skills-hub-ide/skills-hub-py/core/detector.py`

**Step 1: 实现 IDE 探测逻辑**

```python
from pathlib import Path
from .config import HOME, IDE_CANDIDATES
from .utils import log_info

def detect_ides():
    """
    扫描本机已安装的有效 IDE 路径
    返回: List[Dict] -> [{'name': 'Trae', 'path': Path object}, ...]
    """
    found_ides = []
    log_info("正在扫描本机 AI IDE 环境...")

    for name, rel_path in IDE_CANDIDATES:
        full_path = HOME / rel_path
        # 检查目录是否存在 (或者父目录存在，允许我们创建 skills 子目录)
        # 这里策略是：如果 IDE 主目录存在 (e.g. ~/.trae)，我们就认为它有效
        ide_root = full_path.parent

        if ide_root.exists() and ide_root.is_dir():
            # 确保 skills 子目录存在
            if not full_path.exists():
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    log_info(f"  - {name}: 创建目录 {full_path}")
                except Exception as e:
                    log_info(f"  - {name}: 无法创建目录 ({e})，跳过")
                    continue

            found_ides.append({
                "name": name,
                "path": full_path
            })
            log_info(f"  - 发现: {name} -> {full_path}")

    if not found_ides:
        log_info("  - 未发现任何已知 IDE 环境")

    return found_ides
```

**Step 2: Commit**

```bash
git add skills-hub-ide/skills-hub-py/core/detector.py
git commit -m "feat: implement ide detector"
```

---

### Task 3: 核心链接器 (Linker)

**Files:**

- Create: `skills-hub-ide/skills-hub-py/core/linker.py`

**Step 1: 实现跨平台软链接逻辑**

```python
import os
import sys
from pathlib import Path
from .utils import log_info, log_warn, log_error
from .config import get_platform

def create_symlink(source: Path, target: Path):
    """
    创建软链接 target -> source
    自动处理 Windows/Unix 差异及已存在的情况
    """
    if not source.exists():
        log_error(f"源路径不存在: {source}")
        return False

    if target.exists() or target.is_symlink():
        # 如果是同名且指向相同，跳过
        if target.is_symlink() and os.readlink(target) == str(source):
            log_info(f"  [跳过] 链接已存在且正确: {target.name}")
            return True
        else:
            log_warn(f"  [跳过] 目标位置已被占用: {target.name}")
            return False

    try:
        platform = get_platform()
        if platform == 'windows':
            import ctypes
            k32 = ctypes.windll.kernel32
            # Windows 需要管理员权限或者是开发者模式
            # 这里尝试使用 os.symlink (Python 3.8+ 在 Win10 开发者模式下可用)
            try:
                os.symlink(source, target)
            except OSError:
                # 降级尝试: 提示用户权限问题
                log_error("Windows 下创建软链接失败，请尝试以管理员身份运行终端。")
                return False
        else:
            os.symlink(source, target)

        log_info(f"  [成功] 链接创建: {target.name} -> {source}")
        return True
    except Exception as e:
        log_error(f"创建链接失败: {e}")
        return False

def ensure_hub_exists(hub_path: Path):
    if not hub_path.exists():
        try:
            hub_path.mkdir(parents=True, exist_ok=True)
            log_info(f"初始化中转站: {hub_path}")
        except Exception as e:
            log_error(f"无法创建中转站目录: {e}")
```

**Step 2: Commit**

```bash
git add skills-hub-ide/skills-hub-py/core/linker.py
git commit -m "feat: implement cross-platform linker"
```

---

### Task 4: 主程序 (Main CLI)

**Files:**

- Modify: `skills-hub-ide/skills-hub-py/main.py`

**Step 1: 实现 install 命令**

```python
import argparse
import sys
from pathlib import Path
from core.config import AGENTS_HUB
from core.detector import detect_ides
from core.linker import create_symlink, ensure_hub_exists
from core.utils import log_info, log_error

def install_skill(source_path_str: str):
    source_path = Path(source_path_str).resolve()
    skill_name = source_path.name

    log_info(f"=== 开始安装 Skill: {skill_name} ===")

    # 1. 确保中转站存在
    ensure_hub_exists(AGENTS_HUB)

    # 2. 链接到中转站 (Source -> Hub)
    hub_target = AGENTS_HUB / skill_name
    log_info("步骤 1/2: 链接到中转站...")
    if not create_symlink(source_path, hub_target):
        # 如果链接到 Hub 失败（且不是因为已存在），则中止
        # (create_symlink 内部会处理已存在的情况并返回 True/False，这里需根据逻辑微调)
        # 简单策略：只要 target 最终指向正确或存在，我们就继续
        if not (hub_target.exists() and hub_target.is_symlink()):
             log_error("无法链接到中转站，安装中止。")

    # 3. 探测 IDE 并分发 (Hub -> IDEs)
    log_info("步骤 2/2: 分发到 IDE...")
    ides = detect_ides()

    for ide in ides:
        ide_name = ide['name']
        ide_skills_dir = ide['path']
        final_target = ide_skills_dir / skill_name

        # 注意：这里源是指向 Hub 中的那个链接，还是原始源？
        # 最佳实践：指向 Hub 中的链接，这样 Hub 变了（比如重构），IDE 不用变。
        # 但软链接指向软链接在某些系统可能有解析开销。
        # 简单起见：直接指向原始源 (Source -> IDE)，或者指向 Hub (Hub -> IDE)。
        # 这里的架构设计是 "Hub 是中转站"，所以理应是 Hub -> IDE。
        # 但为了避免链式软链接断裂风险，指向 Hub 的绝对路径是比较稳妥的。
        create_symlink(hub_target, final_target)

    log_info("=== 安装完成 ===")

def main():
    parser = argparse.ArgumentParser(description="AI Agent Skill Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install a skill from local path")
    install_parser.add_argument("path", help="Path to the skill source directory")

    args = parser.parse_args()

    if args.command == "install":
        install_skill(args.path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

**Step 2: Commit**

```bash
git add skills-hub-ide/skills-hub-py/main.py
git commit -m "feat: implement main cli install command"
```

---

### Task 5: 验证与文档

**Files:**

- Create: `skills-hub-ide/skills-hub-py/README.md`
- Modify: `skills-hub-ide/README.md` (更新总文档指向)

**Step 1: 编写 Python 版文档**

````markdown
# Agent Skill Manager (Python)

跨平台的 AI 技能管理工具。

## 用法

```bash
python3 main.py install /path/to/your/skill
```
````

## 开发者

...

````

**Step 2: Commit**

```bash
git add skills-hub-ide/skills-hub-py/README.md
git commit -m "docs: add python version documentation"
````

---

### Task 6: 封装为 Trae Skill

**Goal:** 将 Python 工具封装为标准的 Trae Skill，使其能被 AI 助手直接调用（或引导用户调用）。

**Files:**

- Create: `.trae/skills/agent-skills-manager/SKILL.md`
- Move: `skills-hub-ide/skills-hub-py/*` -> `.trae/skills/agent-skills-manager/scripts/`

**Step 1: 迁移代码到 Skill 目录**

为了符合 Trae Skill 规范，我们将代码移动到 `.trae/skills` 下。

```bash
mkdir -p .trae/skills/agent-skills-manager/scripts
cp -r skills-hub-ide/skills-hub-py/* .trae/skills/agent-skills-manager/scripts/
```

**Step 2: 创建 `SKILL.md` 定义文件**

````markdown
---
name: "agent-skills-manager"
description: "Automatically installs and links local agent skills to available IDEs (Trae, Antigravity). Invoke when user wants to install, add, or link a local skill."
---

# Agent Skills Manager

This skill manages the installation and distribution of local AI agent skills.
It automatically detects installed IDEs (Trae, Antigravity) and links the skill source to them via a central hub (~/.agents/skills).

## Usage

When you want to install a local skill directory:

```bash
# Execute using the path to the installed skill script
python3 <skill-install-path>/scripts/main.py install <path-to-skill-source>

# Example (if installed in .trae):
# python3 .trae/skills/agent-skills-manager/scripts/main.py install ./my-new-skill
```
````

## Parameters

- `path-to-skill-source`: The absolute or relative path to the local directory containing the skill source code.

## ⚠️ Important for AI Agents

**Sandbox Restriction**:
This skill requires write permissions to the user's home directory (`~/.agents`). Most AI environments (like Trae/Antigravity) run in a secure sandbox that **blocks** these writes.

**Protocol**:
If you are an AI Agent assisting a user:

1.  **DO NOT** execute the `install` command directly if you suspect you are sandboxed.
2.  **INSTEAD**, construct the correct command using absolute paths.
3.  **PRESENT** the command to the user and ask them to run it in their local terminal (outside the IDE's AI chat).

## Troubleshooting

- Ensure Python 3 is installed.
- On Windows, run the terminal as Administrator if symlink creation fails.

````

**Step 3: 安全性增强 (Sandbox Awareness)**

更新 `core/linker.py` 以处理沙盒环境下的权限错误 (Errno 1)。

```python
    except OSError as e:
        if e.errno == 1:
            log_error(f"权限不足或操作被拒绝 (Errno 1): {e}")
            log_error("如果您在受限环境（如 IDE 内置终端）中运行，请尝试在外部系统终端中运行此命令。")
        else:
            log_error(f"创建链接失败: {e}")
        return False
````

**Step 4: Commit**

```bash
git add .trae/skills/agent-skills-manager
git commit -m "feat: encapsulate as trae skill and handle sandbox restrictions"
```
