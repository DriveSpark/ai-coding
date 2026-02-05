import os
import sys
from pathlib import Path
from .utils import log_info, log_warn, log_error
from .config import get_platform

def create_symlink(source: Path, target: Path):
    """
    创建软链接 target -> source
    自动处理 Windows/Unix 差异及已存在的情况
    """
    if not source.exists():
        log_error(f"源路径不存在: {source}")
        return False

    if target.exists() or target.is_symlink():
        # 如果是同名且指向相同，跳过
        try:
            # os.readlink 可能抛出异常如果不是 link
            if target.is_symlink() and os.readlink(target) == str(source):
                log_info(f"  [跳过] 链接已存在且正确: {target.name}")
                return True
            else:
                log_warn(f"  [跳过] 目标位置已被占用: {target.name}")
                return False
        except OSError:
            log_warn(f"  [跳过] 目标位置已被占用且无法读取链接: {target.name}")
            return False

    try:
        platform = get_platform()
        if platform == 'windows':
            # Windows 需要管理员权限或者是开发者模式
            # 这里尝试使用 os.symlink (Python 3.8+ 在 Win10 开发者模式下可用)
            try:
                os.symlink(source, target)
            except OSError:
                # 降级尝试: 提示用户权限问题
                log_error("Windows 下创建软链接失败，请尝试以管理员身份运行终端。")
                return False
        else:
            os.symlink(source, target)
            
        log_info(f"  [成功] 链接创建: {target.name} -> {source}")
        return True
    except Exception as e:
        log_error(f"创建链接失败: {e}")
        return False

def ensure_hub_exists(hub_path: Path):
    if not hub_path.exists():
        try:
            hub_path.mkdir(parents=True, exist_ok=True)
            log_info(f"初始化中转站: {hub_path}")
        except Exception as e:
            log_error(f"无法创建中转站目录: {e}")
