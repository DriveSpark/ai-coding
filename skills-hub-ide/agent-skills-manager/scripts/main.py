import argparse
import sys
from pathlib import Path
from core.config import AGENTS_HUB
from core.detector import detect_ides
from core.linker import create_symlink, ensure_hub_exists
from core.utils import log_info, log_error

def is_skill_dir(path: Path) -> bool:
    """判断一个目录是否是有效的 Skill (包含 SKILL.md 或 skill.json)"""
    return (path / "SKILL.md").exists() or (path / "skill.json").exists()

def _install_single_skill(source_path: Path):
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
         return # Batch 模式下不要直接 exit

    # 3. 探测 IDE 并分发 (Hub -> IDEs)
    log_info("步骤 2/2: 分发到 IDE...")
    ides = detect_ides()
    
    for ide in ides:
        ide_name = ide['name']
        ide_skills_dir = ide['path']
        final_target = ide_skills_dir / skill_name
        
        # 使用 Hub 中的路径作为源，实现 Source -> Hub -> IDE 的链路
        create_symlink(hub_target, final_target)

    log_info(f"=== 安装完成: {skill_name} ===")

def process_install_path(source_path_str: str):
    path = Path(source_path_str).resolve()
    
    if not path.exists():
        log_error(f"路径不存在: {path}")
        return

    # Case 1: 目标本身就是一个 Skill
    if is_skill_dir(path):
        _install_single_skill(path)
        return

    # Case 2: 目标是一个包含多个 Skills 的父目录
    log_info(f"检测到 '{path.name}' 未包含 Skill 定义文件，尝试扫描子目录...")
    found_skills = []
    
    # 扫描一级子目录
    try:
        for child in path.iterdir():
            if child.is_dir() and not child.name.startswith('.'): # 忽略隐藏目录
                if is_skill_dir(child):
                    found_skills.append(child)
    except Exception as e:
        log_error(f"扫描目录失败: {e}")
        return

    if found_skills:
        log_info(f"发现 {len(found_skills)} 个潜在的 Skills，开始批量安装...")
        success_count = 0
        for skill_path in found_skills:
            print("\n" + "-" * 40)
            try:
                _install_single_skill(skill_path)
                success_count += 1
            except Exception as e:
                log_error(f"安装 {skill_path.name} 时发生错误: {e}")
        
        print("\n" + "=" * 40)
        log_info(f"批量安装结束。成功: {success_count}/{len(found_skills)}")
    else:
        log_error(f"在 '{path}' 下未发现有效的 Skill (需包含 SKILL.md 或 skill.json)")

def main():
    parser = argparse.ArgumentParser(description="AI Agent Skill Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install a skill or a directory of skills")
    install_parser.add_argument("path", help="Path to the skill source directory or parent directory")
    
    args = parser.parse_args()
    
    if args.command == "install":
        process_install_path(args.path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
