from dataclasses import dataclass

from src.settings import API_BASE_URL

AUTH_URL = f"{API_BASE_URL}/api/auth"


@dataclass
class AuthURL:
    base_url: str = AUTH_URL
    id_login: str = f"{base_url}/login/"
    logout: str = f"{base_url}/token/logout/"
    verify: str = f"{base_url}/token/verify/"
    # google login url
    google_login: str = f"{API_BASE_URL}/accounts/google/login/"
    # seesions
    session_create: str = f"{base_url}/session-create/"

    @staticmethod
    def login_session(session_id: str) -> str:
        return f"{AUTH_URL}/login-session/{session_id}/"

    @staticmethod
    def session_token(session_id: str) -> str:
        return f"{AUTH_URL}/session-token/{session_id}/"
