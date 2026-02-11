# 全局技能配置系统说明文档 (GLOBAL_SKILLS)

本文档说明了本项目采用的 AI 技能自动发现与激活机制。通过配置 `global-skills.md` 和 `.cursorrules`，我们实现了一套跨 IDE (Trae, Cursor, Windsurf, Cline) 的通用技能协议。

## 1. 核心文件概览

| 文件名                 | 作用                                                                     | 目标受众       |
| :--------------------- | :----------------------------------------------------------------------- | :------------- |
| **`global-skills.md`** | **技能注册表**。定义了用户意图 (Trigger) 与具体技能 (Skill) 的映射关系。 | AI Agent (LLM) |
| **`.cursorrules`**     | **系统引导指令**。强制 AI 在会话开始时读取注册表，加载项目偏好。         | AI IDE 系统    |

---

## 2. `global-skills.md` (技能协议)

这是项目的核心大脑。它告诉 AI：“当用户想做 X 时，请使用工具 Y”。

### 结构说明

文件按领域分类（视频、开发、文档等），采用 Markdown 表格格式，确保 LLM 易于解析。

**字段定义：**

- **Skill Name**: 技能的标准名称（对应 `.trae/skills/` 下的目录名或内置工具名）。
- **Triggers (Intent)**: 触发该技能的关键词或用户意图。例如：“下载视频”、“download video”。
- **Action / Context Path**: AI 应执行的具体动作和参考路径。

### 示例

```markdown
## 🎥 Video & Media

| Skill Name         | Triggers (Intent)                     | Action / Context Path                                        |
| :----------------- | :------------------------------------ | :----------------------------------------------------------- |
| **`yt-dlp-skill`** | download video, 提取视频, youtube下载 | Use tool: `yt-dlp-skill`<br>Ref: `.trae/skills/yt-dlp-skill` |
```

**如何扩展：**
如果您安装了新技能（例如 `sql-helper`），只需在 `global-skills.md` 中新增一行即可：
`| **sql-helper** | sql query, database, 查库 | Use tool: `sql-helper` |`

---

## 3. `.cursorrules` (自动激活)

这是连接 AI IDE 与技能协议的桥梁。目前大多数 AI 编程工具（Cursor, Windsurf, Cline 等）都会自动读取项目根目录下的 `.cursorrules` 文件作为系统提示词 (System Prompt) 的一部分。

### 核心指令

文件中包含以下关键指令，强制 AI 遵守协议：

1.  **Mandatory Scan**: "At the beginning of every session... READ the file `global-skills.md`"（每次会话开始必读技能表）。
2.  **Strict Mapping**: "If user says 'download video', you MUST use `yt-dlp-skill`"（严格遵循映射关系）。
3.  **Project Preferences**: 定义了中文回复、代码风格等全局偏好。

---

## 4. 快速使用指南

### 在新项目中使用

想让其他项目也拥有这套“智能技能识别”功能？

1.  复制 `global-skills.md` 到新项目根目录。
2.  复制 `.cursorrules` 到新项目根目录。
3.  (可选) 如果有自定义技能，确保 `.trae/skills/` 或相应目录存在。

### 在不同 IDE 中生效

- **Trae**: 自动支持。建议配合 `Core Memory` (核心记忆) 使用效果更佳。
- **Cursor**: 自动读取 `.cursorrules`，开箱即用。
- **Windsurf / Cline**: 同样支持读取根目录规则文件。

---

## 5. 维护建议

- **定期更新 `global-skills.md`**：每当您通过 `npx skills add` 安装了新技能，记得在列表中登记，否则 AI 可能不知道它的存在。
- **保持 `.cursorrules` 简洁**：尽量不要在 `.cursorrules` 里写太具体的业务逻辑，保持它作为一个“引导加载器”的角色，具体的知识放在 `global-skills.md` 或文档中。
