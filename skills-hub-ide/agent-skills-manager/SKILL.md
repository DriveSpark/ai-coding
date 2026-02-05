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

## Parameters

- `path-to-skill-source`: The absolute or relative path to the local directory containing the skill source code.

## Behavior

1.  **Hub Linking**: Links the source directory to `~/.agents/skills/<skill-name>`.
2.  **IDE Detection**: Scans for known IDE configuration directories (e.g., `~/.trae`, `~/.gemini/antigravity`).
3.  **Distribution**: Creates symbolic links from the Hub to each detected IDE's skills directory.

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
