# MacOS 技能管理工具使用指南

本目录包含用于 AI Agent 技能管理的 Bash 脚本工具，支持批量创建软链接、跨 IDE 分发技能。

---

## 📁 文件结构

```
MacOS/
├── link.sh                    # 核心软链接创建工具
├── skills_manager.sh          # 全局技能分发管理器
└── simplebak/
    └── batch_skills_symlink.sh  # 早期版本（备份）
```

---

## 🔧 工具一：`link.sh` - 核心软链接创建工具

### 功能概述
批量将源目录下的所有子文件夹以软链接形式同步到目标目录，同名项会自动跳过。

### 使用方式

#### 方式 1：交互式运行（适合新手）

```bash
# 1. 赋予执行权限（首次使用）
chmod +x link.sh

# 2. 运行脚本
./link.sh
```

**交互流程**：
1. 输入源路径（skills 源码目录）
2. 输入目标路径（直接回车使用默认值 `~/.agents/skills`）
3. 确认执行（输入 `y`）
4. 查看执行结果

#### 方式 2：命令行运行（推荐）

```bash
./link.sh -s <源路径> -t <目标路径> [-y]
```

**参数说明**：
| 参数 | 说明 | 示例 |
|------|------|------|
| `-s, --source` | 源文件夹路径 | `-s ./skills-center` |
| `-t, --target` | 目标文件夹路径 | `-t ~/.agents/skills` |
| `-y, --yes` | 静默模式（自动确认） | `-y` |
| `-h, --help` | 显示帮助信息 | `-h` |

**示例命令**：

```bash
# 把 skills-center 下的技能链接到 .agents/skills（静默模式）
./link.sh -s ./skills-center -t ~/.agents/skills -y

# 把 yt-dlp 技能链接到 Trae 的技能目录
./link.sh -s ./skills-center/yt-dlp -t ~/.trae/skills -y

# 显示帮助信息
./link.sh --help
```

### 输出示例

```
=== 批量创建软链接工具 ===
这个脚本会把源目录下的所有子文件夹，软链接到目标目录。
如果目标目录已有同名项，会跳过（不覆盖）。

使用命令行参数源路径：./skills-center
目标路径已确认：/Users/mac/.agents/skills

即将执行：
  把 ./skills-center 下的所有子目录
  软链接到 ~/.agents/skills
  （同名跳过）
静默模式：自动确认执行。

>> 正在扫描并创建链接...

========================================
           执行结果汇总           
========================================

✅  新增链接 (5):
   + privy
   + yt-dlp
   + skill-seekers
   + vue-disable-linting
   + global-skill-router

⏭️  已存在/跳过 (2):
   • remotion-best-practices
   • test-skill

----------------------------------------
📂 目标目录：/Users/mac/.agents/skills
🎉 完成！
```

### 注意事项

1. **拖拽路径**：从 Finder 拖拽文件夹到终端时，路径会自动加引号，脚本会自动处理
2. **软链接特性**：修改源文件后，链接会自动生效，无需重新创建
3. **跳过策略**：已存在的同名项不会被覆盖，保护现有数据

---

## 🚀 工具二：`skills_manager.sh` - 全局技能分发管理器

### 功能概述
完整的技能生命周期管理工具，支持两阶段同步和多 IDE 分发。

**工作流程**：
```
Source（你的源码） 
   ↓
Hub（中转站 ~/.agents/skills）
   ↓
IDEs（Trae, Antigravity 等）
```

### 支持的 IDE

| IDE 名称 | 目标路径 |
|---------|---------|
| Trae | `~/.trae/skills` |
| Antigravity | `~/.gemini/antigravity/global_skills` |

### 使用步骤

```bash
# 1. 赋予执行权限（首次使用）
chmod +x skills_manager.sh

# 2. 运行脚本
./skills_manager.sh
```

### 交互界面操作

运行后会看到交互式菜单：

```
=== 🚀 AI Skills 全局分发系统 ===

>> 正在同步 Source -> Hub 中转站...
Source: /Users/mac/Desktop/Ai-coding/ai-coding/skills-center
Hub:    /Users/mac/.agents/skills

✅ Hub 中转站同步完成！
---------------------------------------------------------

>> 准备分发到各个 IDE...

=== 请选择要同步的目标 IDE ===
↑/↓: 移动光标 | 空格：选中/取消 | 回车：确认执行 | ESC/q: 退出

当前选中：(无)
----------------------------------------
> ○ Trae -> /Users/mac/.trae/skills
  ○ Antigravity -> /Users/mac/.gemini/antigravity/global_skills
```

**按键操作**：
- **↑↓ 方向键**：上下移动光标
- **空格键**：选中/取消当前项（选中后显示绿色圆点 ●）
- **回车键**：确认执行
- **ESC 或 q**：退出程序

### 完整示例流程

```bash
$ ./skills_manager.sh

请输入源文件夹路径（您的真实 Skills 源码库，支持拖拽）：
源路径：/Users/mac/Desktop/Ai-coding/ai-coding/skills-center

=== 🚀 AI Skills 全局分发系统 ===

>> 正在同步 Source -> Hub 中转站...
Source: /Users/mac/Desktop/Ai-coding/ai-coding/skills-center
Hub:    /Users/mac/.agents/skills

========================================
           执行结果汇总           
========================================

✅  新增链接 (5):
   + privy
   + yt-dlp
   + skill-seekers
   + vue-disable-linting
   + global-skill-router

✨  没有跳过的项
✨  没有跳过的项

----------------------------------------
📂 目标目录：/Users/mac/.agents/skills
🎉 完成！
✅ Hub 中转站同步完成！
---------------------------------------------------------

>> 准备分发到各个 IDE...

[进入交互式菜单，选择要分发的 IDE]

>> 开始同步选中的 1 个目标...

>> 正在分发给 Trae ...
✅ Trae 同步成功！

🎉 所有任务执行完毕！
```

### 高级用法

#### 只同步到 Hub，不分发到 IDE

在交互菜单中不按空格选中任何项，直接按回车即可跳过分发步骤。

#### 同时分发到多个 IDE

用空格键选中多个 IDE，然后按回车确认。

---

## 📋 工具对比

| 功能 | `batch_skills_symlink.sh` | `link.sh` | `skills_manager.sh` |
|------|--------------------------|-----------|---------------------|
| 基础软链接 | ✅ | ✅ | ✅ |
| 命令行参数 | ❌ | ✅ | ❌ |
| 静默模式 | ❌ | ✅ | ✅（内部调用） |
| 多 IDE 分发 | ❌ | ❌ | ✅ |
| 交互式菜单 | ❌ | 可选 | ✅ |
| Hub 中转站 | ❌ | ❌ | ✅ |
| 适用场景 | 简单同步 | 快速同步 | 全局管理 |

---

## 🛠️ 常见问题

### Q1: 什么是软链接？
软链接（Symbolic Link）类似于 Windows 的快捷方式，是一个指向源文件的链接。修改源文件后，通过软链接访问的内容也会更新。

### Q2: 为什么要用 Hub 中转站？
Hub 中转站（`~/.agents/skills`）作为统一的技能仓库，可以：
- 集中管理所有技能
- 避免多次重复同步源码
- 方便扩展到更多 IDE

### Q3: 如何验证软链接是否成功？

```bash
# 查看目标目录的软链接列表
ls -l ~/.agents/skills | grep '^l'

# 查看具体某个技能的链接信息
ls -l ~/.agents/skills/privy
```

输出示例：
```
lrwxr-xr-x  1 mac  staff  68 Feb  9 10:30 privy -> /Users/mac/Desktop/Ai-coding/ai-coding/skills-center/privy
```

### Q4: 如何删除软链接？

```bash
# 删除单个软链接
rm ~/.agents/skills/privy

# 删除所有软链接（谨慎操作）
rm ~/.agents/skills/*
```

### Q5: 脚本报错 "Permission denied" 怎么办？

```bash
# 赋予执行权限
chmod +x link.sh
chmod +x skills_manager.sh
```

### Q6: 如何添加新的 IDE 支持？

编辑 `skills_manager.sh`，找到第 36-39 行：

```bash
IDE_PATHS=(
  "Trae:$HOME/.trae/skills"
  "Antigravity:$HOME/.gemini/antigravity/global_skills"
)
```

添加新的 IDE 配置：
```bash
IDE_PATHS=(
  "Trae:$HOME/.trae/skills"
  "Antigravity:$HOME/.gemini/antigravity/global_skills"
  "YourIDE:$HOME/.youride/skills"
)
```

---

## 📝 最佳实践

### 推荐工作流

1. **开发阶段**：在源码目录（如 `skills-center/`）中开发技能
2. **测试阶段**：使用 `link.sh` 快速链接到测试环境
3. **部署阶段**：使用 `skills_manager.sh` 分发到所有 IDE

### 目录规划建议

```
~/Desktop/Ai-coding/ai-coding/
├── skills-center/          # 技能源码（Git 仓库）
│   ├── privy/
│   ├── yt-dlp/
│   └── ...
├── skills-hub-ide/
│   └── MacOS/
│       ├── link.sh
│       └── skills_manager.sh
└── .agents/skills/         # Hub 中转站（隐藏目录）
```

### 版本控制

- ✅ 将技能源码纳入 Git 管理
- ❌ 不要将 Hub 目录或 IDE 目录纳入 Git（这些是生成的软链接）

在 `.gitignore` 中添加：
```
.agents/
.trae/
.gemini/
```

---

## 🔗 相关资源

- [项目总览](../../README.md)
- [Agent Skills Manager Python 版](../docs/plans/)
- [Windows 版本工具](../Windows/link.ps1)

---

**最后更新**: 2026-03-09  
**维护者**: AI Coding Team
