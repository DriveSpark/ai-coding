import sys
import tty
import termios
import os
from .utils import CYAN, GREEN, BOLD, RESET, log_warn

class Key:
    UP = 'UP'
    DOWN = 'DOWN'
    ENTER = 'ENTER'
    SPACE = 'SPACE'
    ESC = 'ESC'
    OTHER = 'OTHER'

def get_key():
    """读取单个按键，支持识别箭头键"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':  # ESC sequence
            # 设置非阻塞读取后续字符
            import select
            dr, dw, de = select.select([sys.stdin], [], [], 0.1)
            if not dr:
                return Key.ESC
            
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                if ch3 == 'A': return Key.UP
                if ch3 == 'B': return Key.DOWN
            return Key.OTHER
        elif ch == '\r' or ch == '\n':
            return Key.ENTER
        elif ch == ' ':
            return Key.SPACE
        elif ch == '\x03': # Ctrl+C
            raise KeyboardInterrupt
        else:
            return Key.OTHER
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def clear_screen():
    os.system('clear')

def interactive_select(options, title="请选择目标"):
    """
    交互式多选菜单
    options: [{'name': 'Trae', 'path': Path, ...}, ...]
    返回: 选中的 options 列表
    """
    if not options:
        return []

    selected = [False] * len(options)
    # 默认全选 (如果用户希望默认全选的话，或者默认都不选？Bash脚本里好像是默认不选或者记住上次？
    # 用户需求：直接回车默认，那应该是有一个确认步骤。
    # 让我们模仿 Bash 脚本：默认可能不选，或者全选。Bash 脚本里逻辑是默认全选吗？
    # Bash 脚本里: selected=([true] [true] ...) 默认是全选的。
    selected = [True] * len(options) 
    
    current = 0
    
    while True:
        clear_screen()
        print(f"{BOLD}{CYAN}=== {title} ==={RESET}")
        print(f"↑/↓: 移动光标 | 空格: 选中/取消 | 回车: 确认执行")
        print("-" * 40)
        
        # 显示列表
        for idx, option in enumerate(options):
            name = option['name']
            path = option['path']
            
            # 选中标记
            mark = f"{GREEN}●{RESET}" if selected[idx] else "○"
            
            # 光标标记
            if idx == current:
                prefix = f"{BOLD}{CYAN}> {RESET}"
                line = f"{prefix}{mark} {BOLD}{name}{RESET} -> {path}"
            else:
                prefix = "  "
                line = f"{prefix}{mark} {name} -> {path}"
            
            print(line)
            
        # 打印当前选中汇总
        selected_names = [opt['name'] for i, opt in enumerate(options) if selected[i]]
        if selected_names:
            print("-" * 40)
            print(f"当前选中: {GREEN}{', '.join(selected_names)}{RESET}")
        else:
            print("-" * 40)
            print("当前选中: (无)")
            
        key = get_key()
        
        if key == Key.UP:
            current = (current - 1) % len(options)
        elif key == Key.DOWN:
            current = (current + 1) % len(options)
        elif key == Key.SPACE:
            selected[current] = not selected[current]
        elif key == Key.ENTER:
            break
        elif key == Key.ESC:
            print("\n已取消。")
            sys.exit(0)
            
    return [opt for i, opt in enumerate(options) if selected[i]]

def confirm_action(question):
    """简单的是/否确认"""
    while True:
        choice = input(f"{question} [Y/n] ").strip().lower()
        if choice in ['', 'y', 'yes']:
            return True
        if choice in ['n', 'no']:
            return False
