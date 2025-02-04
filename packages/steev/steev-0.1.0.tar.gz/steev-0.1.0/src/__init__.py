# This file can be empty, it's just to make the directory a Python package

import os

from src.settings import CACHE_FILE, LOCAL_DIR

# Create .steev directory in user's home directory
if not os.path.exists(LOCAL_DIR):
    LOCAL_DIR.mkdir(exist_ok=True)
    # Set directory permissions to 700 (rwx------)
    # This means only the owner can read, write, or access the directory
    os.chmod(LOCAL_DIR, 0o700)

if not os.path.exists(CACHE_FILE):
    CACHE_FILE.touch()
    os.chmod(CACHE_FILE, 0o600)  # Set file permissions to 600 (rw-------)

__version__ = "0.0.0"


# ANSI escape codes for colors
CYAN = "\033[96m"
WHITE = "\033[97m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
BROWN = "\033[33m"
RESET = "\033[0m"
BOLD = "\033[1m"

STEEV_LOGO: str = f"""
{CYAN}{BOLD}╔════════════════════════════════════════════════════╗
║    {WHITE}███████╗████████╗███████╗███████╗██╗   ██╗      {CYAN}║
║    {WHITE}██╔════╝╚══██╔══╝██╔════╝██╔════╝██║   ██║      {CYAN}║
║    {WHITE}███████╗   ██║   █████╗  █████╗  ██║   ██║      {CYAN}║
║    {WHITE}╚════██║   ██║   ██╔══╝  ██╔══╝  ██║   ██║      {CYAN}║
║    {WHITE}███████║   ██║   ███████╗███████╗╚██████╔╝      {CYAN}║
║    {WHITE}╚══════╝   ╚═╝   ╚══════╝╚══════╝ ╚═════╝       {CYAN}║
║                                                    {CYAN}║
║    {GREEN}Your Ultimate AI Training Assistant{CYAN}             ║
╚════════════════════════════════════════════════════╝{RESET}"""

print(STEEV_LOGO)
