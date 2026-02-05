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
    
    # 尝试链接到 Hub
    link_success = create_symlink(source_path, hub_target)
    
    # 如果 create_symlink 返回 False，可能是因为已存在（在 linker 里是 warn）或者失败
    # 我们需要确认 target 是否有效可用
    if not (hub_target.exists() or (hub_target.is_symlink() and hub_target.exists())):
         log_error("无法链接到中转站，安装中止。")

    # 3. 探测 IDE 并分发 (Hub -> IDEs)
    log_info("步骤 2/2: 分发到 IDE...")
    ides = detect_ides()
    
    for ide in ides:
        ide_name = ide['name']
        ide_skills_dir = ide['path']
        final_target = ide_skills_dir / skill_name
        
        # 使用 Hub 中的路径作为源，实现 Source -> Hub -> IDE 的链路
        # 这样以后如果 Source 变了，只要改 Hub 这里的 link，IDE 那边不用动（如果是软链到软链）
        # 但为了兼容性，直接链到 hub_target (即 ~/.agents/skills/xxx)
        create_symlink(hub_target, final_target)

    log_info(f"=== 安装完成: {skill_name} ===")

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
