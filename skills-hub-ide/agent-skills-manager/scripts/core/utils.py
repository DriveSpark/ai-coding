import sys

def log_info(msg):
    print(f"[\033[92mINFO\033[0m] {msg}")

def log_warn(msg):
    print(f"[\033[93mWARN\033[0m] {msg}")

def log_error(msg):
    print(f"[\033[91mERROR\033[0m] {msg}")
    sys.exit(1)
