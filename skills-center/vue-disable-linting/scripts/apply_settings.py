import os
import json
import sys

def detect_project_features(root_dir):
    """
    Detects project features based on files and package.json.
    Returns a set of feature tags.
    """
    features = set()
    
    package_json_path = os.path.join(root_dir, 'package.json')
    dependencies = {}
    devDependencies = {}
    
    if os.path.exists(package_json_path):
        try:
            with open(package_json_path, 'r') as f:
                pkg = json.load(f)
                dependencies = pkg.get('dependencies', {})
                devDependencies = pkg.get('devDependencies', {})
        except:
            pass
            
    all_deps = {**dependencies, **devDependencies}
    
    # Check for ESLint
    if 'eslint' in all_deps or any(f.startswith('.eslintrc') for f in os.listdir(root_dir)):
        features.add('eslint')
        
    # Check for Stylelint
    if 'stylelint' in all_deps or any(f.startswith('.stylelintrc') for f in os.listdir(root_dir)):
        features.add('stylelint')
        
    # Check for Vue
    if 'vue' in all_deps or any(f.endswith('.vue') for f in os.listdir(root_dir)):
        features.add('vue')
        
    # Check for TypeScript
    if 'typescript' in all_deps or os.path.exists(os.path.join(root_dir, 'tsconfig.json')):
        features.add('typescript')
        
    # Check for Prettier
    if 'prettier' in all_deps or any(f.startswith('.prettierrc') for f in os.listdir(root_dir)):
        features.add('prettier')

    return features

def apply_settings():
    """
    Creates or updates .vscode/settings.json based on detected project features.
    """
    # Current working directory is assumed to be project root
    root_dir = os.getcwd()
    vscode_dir = os.path.join(root_dir, ".vscode")
    settings_file = os.path.join(vscode_dir, "settings.json")
    
    print(f"🔍 Analyzing project in: {root_dir}")
    features = detect_project_features(root_dir)
    print(f"✅ Detected features: {', '.join(features) if features else 'None'}")

    # Ensure .vscode directory exists
    if not os.path.exists(vscode_dir):
        try:
            os.makedirs(vscode_dir)
        except OSError as e:
            print(f"❌ Error creating directory {vscode_dir}: {e}")
            sys.exit(1)

    # Load existing settings if file exists
    settings = {}
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r') as f:
                content = f.read().strip()
                if content:
                    settings = json.loads(content)
        except json.JSONDecodeError:
            print(f"⚠️  Warning: {settings_file} contains invalid JSON. Will overwrite with new valid JSON.")
        except Exception as e:
            print(f"❌ Error reading {settings_file}: {e}")
            sys.exit(1)

    # Build dynamic settings based on detection
    new_settings = {}

    # Always disable built-in validation for safety in "legacy" mode
    new_settings["javascript.validate.enable"] = False
    
    if 'eslint' in features:
        print("  - Disabling ESLint")
        new_settings["eslint.enable"] = False
        new_settings["editor.codeActionsOnSave"] = settings.get("editor.codeActionsOnSave", {})
        if isinstance(new_settings["editor.codeActionsOnSave"], dict):
            new_settings["editor.codeActionsOnSave"]["source.fixAll.eslint"] = False

    if 'stylelint' in features:
        print("  - Disabling Stylelint")
        new_settings["stylelint.enable"] = False
        new_settings["css.validate"] = False
        new_settings["scss.validate"] = False
        new_settings["less.validate"] = False

    if 'vue' in features:
        print("  - Disabling Vue validations (Vetur/Volar)")
        new_settings["vetur.validation.template"] = False
        new_settings["vetur.validation.script"] = False
        new_settings["vetur.validation.style"] = False
        new_settings["volar.diagnostics.enable"] = False
        
    if 'typescript' in features:
        print("  - Disabling TypeScript validation")
        new_settings["typescript.validate.enable"] = False

    if 'prettier' in features:
        print("  - Disabling Prettier (format on save)")
        # We don't necessarily want to disable formatting if user likes it, 
        # but usually "red lines" come from linters. 
        # If user wants "no changes", disabling formatOnSave is good.
        new_settings["editor.formatOnSave"] = False

    # Update settings
    settings.update(new_settings)

    # Write settings back to file
    try:
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)
        print(f"\n✅ Successfully updated {settings_file}")
        print("💡 Tip: Reload VS Code window (Cmd+Shift+P -> 'Reload Window') to apply changes.")
    except Exception as e:
        print(f"❌ Error writing to {settings_file}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    apply_settings()
