import argparse
import sys
from pathlib import Path
from core.config import AGENTS_HUB
from core.detector import detect_ide_candidates
from core.linker import create_symlink, ensure_hub_exists
from core.menu import interactive_select, confirm_action
from core.utils import (
    log_info, log_error, log_success, log_warn, 
    log_header, log_step, BOLD, CYAN, GREEN, RESET
)

def is_skill_dir(path: Path) -> bool:
    """判断一个目录是否是有效的 Skill (包含 SKILL.md 或 skill.json)"""
    return (path / "SKILL.md").exists() or (path / "skill.json").exists()

def prepare_ide_environment():
    """
    检测并准备 IDE 环境 (交互式创建目录)
    """
    log_info("正在扫描本机 AI IDE 环境...")
    candidates = detect_ide_candidates()
    
    if not candidates:
        log_error("未检测到任何已知 IDE 环境 (Trae, Antigravity 等)。")
        sys.exit(1)
        
    available_ides = []
    
    for ide in candidates:
        name = ide['name']
        path = ide['path']
        exists = ide['exists']
        
        if exists:
            log_success(f"发现: {name} -> {path}")
            available_ides.append(ide)
        else:
            # 询问是否创建
            if confirm_action(f"{BOLD}发现 {name} 环境，但缺少 skills 目录。是否创建?{RESET}"):
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    log_success(f"已创建: {path}")
                    ide['exists'] = True
                    available_ides.append(ide)
                except Exception as e:
                    log_error(f"无法创建目录 {path}: {e}")
            else:
                log_warn(f"跳过 {name}")

    if not available_ides:
        log_error("未检测到合适的安装环境，程序退出。")
        sys.exit(1)
        
    return available_ides

def _install_single_skill(source_path: Path, target_ides: list) -> bool:
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
         return False # Batch 模式下不要直接 exit

    # 3. 探测 IDE 并分发 (Hub -> IDEs)
    log_step(2, 2, "分发到选定的 IDE...")
    
    if not target_ides:
        log_info("未选择 IDE，跳过分发步骤。")
        return True # 虽然没分发，但中转站链接成功也算成功的一部分？或者算 True 以继续
    else:
        all_targets_ok = True
        for ide in target_ides:
            ide_name = ide['name']
            ide_skills_dir = ide['path']
            final_target = ide_skills_dir / skill_name
            
            # 使用 Hub 中的路径作为源，实现 Source -> Hub -> IDE 的链路
            if not create_symlink(hub_target, final_target):
                all_targets_ok = False
        
        if all_targets_ok:
             log_success(f"安装完成: {skill_name}")
             return True
        else:
             return False

def process_install_path(source_path_str: str):
    path = Path(source_path_str).resolve()
    
    if not path.exists():
        log_error(f"路径不存在: {path}")
        return

    # 0. 预先探测并准备 IDE 环境
    available_ides = prepare_ide_environment()
    
    # 交互式选择目标 IDE
    target_ides = interactive_select(available_ides, title="请选择要同步的目标 IDE")
    
    if not target_ides:
        log_warn("未选择任何 IDE，将仅安装到中转站。")
    
    if is_skill_dir(path):
        # 单个 Skill 安装
        if _install_single_skill(path, target_ides):
             log_success("单 Skill 安装成功！")
        else:
             log_error("单 Skill 安装失败！")
    else:
        # 批量安装 (扫描子目录)
        log_info(f"路径 {path} 不是标准 Skill 目录，尝试扫描子目录...")
        sub_skills = [p for p in path.iterdir() if p.is_dir() and is_skill_dir(p)]
        
        if not sub_skills:
            log_warn("未在子目录中发现任何有效的 Skill (需包含 SKILL.md 或 skill.json)")
            return
            
        log_info(f"发现 {len(sub_skills)} 个待安装的 Skill")
        
        success_count = 0
        failed_list = []
        
        for skill_path in sub_skills:
            print("-" * 40)
            if _install_single_skill(skill_path, target_ides):
                success_count += 1
            else:
                failed_list.append(skill_path.name)
                
        print("=" * 40)
        log_success(f"批量安装结束。成功: {success_count}/{len(sub_skills)}")
        
        if failed_list:
            log_warn(f"失败列表 ({len(failed_list)}): {', '.join(failed_list)}")
            log_warn("如果遇到权限错误 (Errno 1)，请复制以下命令在外部终端运行：")
            
            # 生成一键修复命令
            cmd_parts = [f"python3 {sys.argv[0]} install {source_path_str}"]
            print(f"\n{BOLD}{CYAN}{' '.join(cmd_parts)}{RESET}\n")

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
