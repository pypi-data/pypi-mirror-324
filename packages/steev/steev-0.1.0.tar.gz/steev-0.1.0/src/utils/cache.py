from dotenv import get_key, set_key, unset_key

from src.settings import CACHE_FILE


def set_cache(key: str, value: str):
    set_key(CACHE_FILE, key, value)


def get_cache(key: str):
    return get_key(CACHE_FILE, key)


def delete_cache(key: str):
    unset_key(CACHE_FILE, key)
