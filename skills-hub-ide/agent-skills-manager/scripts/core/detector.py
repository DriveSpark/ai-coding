from pathlib import Path
from .config import HOME, IDE_CANDIDATES

def detect_ide_candidates():
    """
    扫描本机已安装的有效 IDE 候选路径
    返回: List[Dict] -> [{'name': 'Trae', 'path': Path, 'exists': bool}, ...]
    """
    candidates = []
    
    for name, rel_path in IDE_CANDIDATES:
        full_path = HOME / rel_path
        # 检查 IDE 主配置目录是否存在 (e.g. ~/.trae)
        ide_root = full_path.parent
        
        if ide_root.exists() and ide_root.is_dir():
            candidates.append({
                "name": name,
                "path": full_path,
                "exists": full_path.exists() and full_path.is_dir()
            })
            
    return candidates
