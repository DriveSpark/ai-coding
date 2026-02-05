import sys

# ANSI Colors
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
BLUE = "\033[34m"

def log_info(msg):
    print(f"{GREEN}[INFO]{RESET} {msg}")

def log_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def log_warn(msg):
    print(f"{YELLOW}[WARN]{RESET} {msg}")

def log_error(msg, exit_code=None):
    print(f"{RED}[ERROR]{RESET} {msg}")
    if exit_code is not None:
        sys.exit(exit_code)

def log_header(msg):
    print(f"\n{BOLD}{CYAN}=== {msg} ==={RESET}")

def log_step(step_num, total_steps, msg):
    print(f"{BLUE}Step {step_num}/{total_steps}:{RESET} {msg}")
