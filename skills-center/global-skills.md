# Global Skills Protocol (global-skills.md)

> **SYSTEM INSTRUCTION FOR AI AGENT:**
> You are operating in a project with specialized capabilities.
> **MANDATORY:** Scan this file at the start of every session.
> If a user request matches a **Trigger**, you MUST prioritize using the corresponding **Skill** or **Tool**.

---

## 🛠️ Development & Engineering

| Skill Name                           | Triggers (Intent)                                 | Action / Context Path                      |
| :----------------------------------- | :------------------------------------------------ | :----------------------------------------- |
| **`verification-before-completion`** | done, finished, verify, check work, pre-commit    | Use tool: `verification-before-completion` |
| **`test-driven-development`**        | tdd, write test first, test driven                | Use tool: `test-driven-development`        |
| **`systematic-debugging`**           | debug, fix bug, error analysis, broken            | Use tool: `systematic-debugging`           |
| **`webapp-testing`**                 | playwright, e2e test, browser test, ui test       | Use tool: `webapp-testing`                 |
| **`receiving-code-review`**          | review feedback, address comments, fix pr         | Use tool: `receiving-code-review`          |
| **`requesting-code-review`**         | review my code, pr ready, check implementation    | Use tool: `requesting-code-review`         |
| **`finishing-a-development-branch`** | merge branch, close feature, cleanup branch       | Use tool: `finishing-a-development-branch` |
| **`using-git-worktrees`**            | git worktree, parallel branch, isolated workspace | Use tool: `using-git-worktrees`            |
| **`mcp-builder`**                    | build mcp, mcp server, model context protocol     | Use tool: `mcp-builder`                    |
| **`subagent-driven-development`**    | split tasks, subagents, parallel execution        | Use tool: `subagent-driven-development`    |

## 📄 Documents & Office

| Skill Name            | Triggers (Intent)                                | Action / Context Path       |
| :-------------------- | :----------------------------------------------- | :-------------------------- |
| **`docx`**            | word, docx, create document, edit word           | Use tool: `docx`            |
| **`xlsx`**            | excel, spreadsheet, csv, data analysis           | Use tool: `xlsx`            |
| **`pdf`**             | pdf, read pdf, merge pdf, ocr                    | Use tool: `pdf`             |
| **`pptx`**            | powerpoint, slides, presentation, deck           | Use tool: `pptx`            |
| **`doc-coauthoring`** | write specs, proposal, technical doc, co-author  | Use tool: `doc-coauthoring` |
| **`internal-comms`**  | newsletter, status report, internal update, memo | Use tool: `internal-comms`  |

## 🎨 Design & Creative

| Skill Name                  | Triggers (Intent)                                    | Action / Context Path             |
| :-------------------------- | :--------------------------------------------------- | :-------------------------------- |
| **`frontend-design`**       | ui design, web interface, styling, tailwind          | Use tool: `frontend-design`       |
| **`canvas-design`**         | poster, graphic design, visual art, image generation | Use tool: `canvas-design`         |
| **`web-artifacts-builder`** | complex ui, interactive component, web artifact      | Use tool: `web-artifacts-builder` |
| **`theme-factory`**         | color theme, design system, style guide              | Use tool: `theme-factory`         |
| **`slack-gif-creator`**     | slack gif, animated gif, reaction gif                | Use tool: `slack-gif-creator`     |
| **`algorithmic-art`**       | p5.js, generative art, creative code                 | Use tool: `algorithmic-art`       |
| **`brand-guidelines`**      | brand colors, official style, company branding       | Use tool: `brand-guidelines`      |

## 🧠 Planning & Workflow

| Skill Name                        | Triggers (Intent)                          | Action / Context Path                   |
| :-------------------------------- | :----------------------------------------- | :-------------------------------------- |
| **`brainstorming`**               | brainstorm, ideas, explore, think          | Use tool: `brainstorming`               |
| **`writing-plans`**               | create plan, roadmap, implementation steps | Use tool: `writing-plans`               |
| **`executing-plans`**             | execute plan, run steps, follow guide      | Use tool: `executing-plans`             |
| **`dispatching-parallel-agents`** | parallel tasks, multi-agent, async work    | Use tool: `dispatching-parallel-agents` |

## ⚙️ Skill Management

| Skill Name              | Triggers (Intent)                         | Action / Context Path         |
| :---------------------- | :---------------------------------------- | :---------------------------- |
| **`find-skills`**       | find skill, search tool, how to do X      | Use tool: `find-skills`       |
| **`skill-creator`**     | create skill, new capability, custom tool | Use tool: `skill-creator`     |
| **`writing-skills`**    | edit skill, modify capability, fix skill  | Use tool: `writing-skills`    |
| **`using-superpowers`** | help, guide, how to use skills            | Use tool: `using-superpowers` |

---

## 🚀 Usage Guide for Any AI IDE

### Best Practice (Token Efficient)

If your IDE supports Custom Skills (like Trae), use the `global-skill-router` skill. This allows the agent to "lazy load" the skill map only when needed, saving tokens.

### Standard Setup (Universal)

For IDEs without skill support (Cursor, Windsurf, Cline):

1.  **Ensure this file exists** in the project root: `global-skills.md`
2.  **Add to System Prompt / Custom Instructions**:
    > "Check `global-skills.md` or use `global-skill-router` to understand available tools and their triggers."
