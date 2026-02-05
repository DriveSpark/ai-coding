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
