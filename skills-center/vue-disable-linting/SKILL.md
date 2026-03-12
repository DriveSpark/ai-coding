---
name: disable-linting
description: Instantly disables strict linting rules (ESLint, Vetur, Volar) for the current project by creating a local VS Code configuration. This skill prevents annoying red underlines and build errors in legacy projects without modifying source code. Use it when you want to suppress linting errors in a specific workspace.
---

# Disable Linting Skill

This skill provides a quick way to disable linting and formatting checks in VS Code for the current workspace. It is particularly useful for working with legacy codebases where you do not want to fix hundreds of existing lint errors or modify the project's source code.

## How it Works

The skill runs a script that creates or updates the `.vscode/settings.json` file in your project root. This file contains workspace-specific settings that override global VS Code settings, effectively turning off:

- ESLint
- Vetur validation (template, script, style)
- Volar diagnostics
- TypeScript/JavaScript validation
- Automatic code actions on save (like fixing lint errors)

## Usage

To use this skill, run the provided script in your project root:

```bash
python3 scripts/apply_settings.py
```

After running the script, you may need to reload the VS Code window for changes to take effect:
1. Open Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux)
2. Type `Reload Window` and select it.

## Resources

- **Script**: `scripts/apply_settings.py` - The Python script that generates the configuration.
