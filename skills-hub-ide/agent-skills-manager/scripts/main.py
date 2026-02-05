import argparse
import sys
from pathlib import Path
from core.config import AGENTS_HUB
from core.detector import detect_ides
from core.linker import create_symlink, ensure_hub_exists
from core.utils import (
    log_info, log_error, log_success, log_warn, 
    log_header, log_step, BOLD, CYAN, GREEN, RESET
)

def is_skill_dir(path: Path) -> bool:
    """判断一个目录是否是有效的 Skill (包含 SKILL.md 或 skill.json)"""
    return (path / "SKILL.md").exists() or (path / "skill.json").exists()

def select_target_ides(available_ides: list) -> list:
    """
    交互式让用户选择要安装的 IDE
    """
    if not available_ides:
        log_warn("未检测到任何支持的 IDE，安装可能仅限于中转站。")
        return []

    print(f"\n{BOLD}{CYAN}检测到以下 IDE 环境:{RESET}")
    for idx, ide in enumerate(available_ides):
        print(f"  [{idx + 1}] {GREEN}{ide['name']}{RESET} ({ide['path']})")
    
    print(f"\n{BOLD}请选择要安装的目标 IDE:{RESET}")
    print("  - 输入序号 (如 '1' 或 '1,2')")
    print("  - 输入 'a' 或 'all' 全选")
    print("  - 直接回车默认全选")
    
    choice = input(f"{BOLD}您的选择 > {RESET}").strip().lower()
    
    if choice in ['', 'a', 'all']:
        log_info("已选择: 所有 IDE")
        return available_ides
    
    selected_indices = []
    try:
        parts = choice.replace(',', ' ').split()
        for part in parts:
            idx = int(part) - 1
            if 0 <= idx < len(available_ides):
                selected_indices.append(idx)
            else:
                log_warn(f"忽略无效序号: {part}")
    except ValueError:
        log_error("输入格式无效，请输入数字序号。")
        return []
        
    if not selected_indices:
        log_warn("未选择任何 IDE，将仅安装到中转站。")
        return []
        
    selected_ides = [available_ides[i] for i in selected_indices]
    names = ", ".join([ide['name'] for ide in selected_ides])
    log_info(f"已选择: {names}")
    return selected_ides

def _install_single_skill(source_path: Path, target_ides: list):
    skill_name = source_path.name
    
    log_header(f"安装 Skill: {skill_name}")
    
    # 1. 确保中转站存在
    ensure_hub_exists(AGENTS_HUB)
    
    # 2. 链接到中转站 (Source -> Hub)
    hub_target = AGENTS_HUB / skill_name
    log_step(1, 2, "链接到中转站 (~/.agents/skills)...")
    
    # 尝试链接到 Hub
    link_success = create_symlink(source_path, hub_target)
    
    # 如果 create_symlink 返回 False，可能是因为已存在（在 linker 里是 warn）或者失败
    # 我们需要确认 target 是否有效可用
    if not (hub_target.exists() or (hub_target.is_symlink() and hub_target.exists())):
         log_error("无法链接到中转站，安装中止。")
         return # Batch 模式下不要直接 exit

    # 3. 探测 IDE 并分发 (Hub -> IDEs)
    log_step(2, 2, "分发到选定的 IDE...")
    
    if not target_ides:
        log_info("未选择 IDE，跳过分发步骤。")
    else:
        for ide in target_ides:
            ide_name = ide['name']
            ide_skills_dir = ide['path']
            final_target = ide_skills_dir / skill_name
            
            # 使用 Hub 中的路径作为源，实现 Source -> Hub -> IDE 的链路
            create_symlink(hub_target, final_target)

    log_success(f"安装完成: {skill_name}")

def process_install_path(source_path_str: str):
    path = Path(source_path_str).resolve()
    
    if not path.exists():
        log_error(f"路径不存在: {path}")
        return

    # 0. 预先探测并选择 IDE (只做一次)
    all_ides = detect_ides()
    target_ides = select_target_ides(all_ides)

    # Case 1: 目标本身就是一个 Skill
    if is_skill_dir(path):
        _install_single_skill(path, target_ides)
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
            try:
                _install_single_skill(skill_path, target_ides)
                success_count += 1
            except Exception as e:
                log_error(f"安装 {skill_path.name} 时发生错误: {e}")
        
        print("\n" + "=" * 40)
        log_success(f"批量安装结束。成功: {success_count}/{len(found_skills)}")
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
