import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR.parent / ".env")

DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

LOCAL_DIR = Path.home() / ".steev"
CREDENTIALS_FILE = LOCAL_DIR / "credentials.json"

API_BASE_URL = "https://steev-backend-production.up.railway.app"
WS_BASE_URL = "wss://steev-backend-production.up.railway.app/ws"

CACHE_FILE = LOCAL_DIR / ".cache"
