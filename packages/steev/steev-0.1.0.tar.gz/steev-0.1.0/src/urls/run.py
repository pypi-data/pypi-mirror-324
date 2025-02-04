from dataclasses import dataclass

from src.settings import API_BASE_URL

BASE_URL = f"{API_BASE_URL}/api/experiment"


@dataclass
class RunURL:
    base_url: str = BASE_URL
    register_train: str = f"{base_url}/register/"
