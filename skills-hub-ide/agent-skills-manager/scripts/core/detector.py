from pathlib import Path
from .config import HOME, IDE_CANDIDATES
from .utils import log_info

def detect_ides():
    """
    扫描本机已安装的有效 IDE 路径
    返回: List[Dict] -> [{'name': 'Trae', 'path': Path object}, ...]
    """
    found_ides = []
    log_info("正在扫描本机 AI IDE 环境...")
    
    for name, rel_path in IDE_CANDIDATES:
        full_path = HOME / rel_path
        # 检查目录是否存在 (或者父目录存在，允许我们创建 skills 子目录)
        # 这里策略是：如果 IDE 主目录存在 (e.g. ~/.trae)，我们就认为它有效
        ide_root = full_path.parent
        
        if ide_root.exists() and ide_root.is_dir():
            # 确保 skills 子目录存在
            if not full_path.exists():
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    log_info(f"  - {name}: 创建目录 {full_path}")
                except Exception as e:
                    log_info(f"  - {name}: 无法创建目录 ({e})，跳过")
                    continue
            
            found_ides.append({
                "name": name,
                "path": full_path
            })
            log_info(f"  - 发现: {name} -> {full_path}")
    
    if not found_ides:
        log_info("  - 未发现任何已知 IDE 环境")
        
    return found_ides
