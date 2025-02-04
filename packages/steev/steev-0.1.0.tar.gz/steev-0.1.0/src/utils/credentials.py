import json
import time
from datetime import datetime
from typing import TypedDict

import requests

from src.settings import API_BASE_URL, CREDENTIALS_FILE
from src.utils.log import setup_logger

logger, log_entry = setup_logger(__name__)


class TokenType(TypedDict):
    access_token: str
    refresh_token: str
    access_exp: float | None


class Credential:
    user: str
    email: str
    token: TokenType
    _logged_in: bool

    @log_entry
    def __init__(self):
        self.user = ""
        self.email = ""
        self.token = TokenType(access_token="", refresh_token="", access_exp=0.0)
        self._logged_in = False

        self.load_access_token()

    @property
    def logged_in(self) -> bool:
        return self._logged_in

    @property
    def access_token(self) -> str:
        return self.token["access_token"]

    @property
    def refresh_token(self) -> str:
        return self.token["refresh_token"]

    def __str__(self):
        if self.token["access_exp"] == 0.0 or self.token["access_exp"] is None:
            readable_date = ""
        else:
            readable_date = datetime.fromtimestamp(self.token["access_exp"]).strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"Credential\n"
            f"  user   {self.user}\n"
            f"  email  {self.email}\n"
            f"\n  tokens\n"
            f"    access_token   {self.token['access_token'][:10]}...\n"
            f"    refresh_token  {self.token['refresh_token'][:10]}...\n"
            f"    access_exp     {readable_date}\n"
        )

    @log_entry
    def load_access_token(self) -> bool:
        if not CREDENTIALS_FILE.exists():
            logger.debug("Access token file does not exist, creating one.")
            CREDENTIALS_FILE.touch()
            return False

        with open(CREDENTIALS_FILE, "r") as f:
            content = f.read()
            if not content:
                logger.debug("Access token file is empty")
                return False

            try:
                data = json.loads(content)
                self.user = data["user"]
                self.email = data["email"]
                self.token["access_token"] = data["token"]["access_token"]
                self.token["refresh_token"] = data["token"]["refresh_token"]
                self.token["access_exp"] = data["token"]["access_exp"]
                return True
            except json.JSONDecodeError:
                return False

    @log_entry
    def update_token(self, data: TokenType, save: bool = False):
        self.token = data
        if save:
            self.save()

    @log_entry
    def update_data(self, data: dict, save: bool = False):
        self.user = data["user"]
        self.email = data["email"]
        self.update_token(data["token"], save=save)
        if save:
            self.save()

    @log_entry
    def to_json(self):
        """Convert credential object to JSON-serializable dictionary"""
        return {
            "user": self.user,
            "email": self.email,
            "token": self.token,
        }

    @log_entry
    def save(self):
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(self.to_json(), f)

    @log_entry
    def verify(self) -> bool:
        if self.token["access_token"] == "":
            logger.debug("Access token is empty")
            return False
        url = f"{API_BASE_URL}/api/auth/token/verify/"
        data = {"token": self.token["access_token"]}
        logger.debug(f"Sending request to {url} with data: {data}")
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response text: {response.text}")
        return response.status_code == 200

    @log_entry
    def clear(self):
        self.token["access_token"] = ""
        self.token["refresh_token"] = ""
        self.token["access_exp"] = None
        self.user = ""
        self.email = ""
        self._logged_in = False
        self.save()

    @log_entry
    def is_expired(self) -> bool:
        if self.token["access_exp"] is None:
            return True
        return time.time() > self.token["access_exp"]

    @log_entry
    def refresh(self) -> bool:
        url = f"{API_BASE_URL}/api/auth/token/refresh/"
        data = {"refresh": self.token["refresh_token"]}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            return False
        access_token = response.json()["access"]
        new_token: TokenType = {
            "access_token": access_token,
            "refresh_token": self.token["refresh_token"],
            "access_exp": extract_exp(access_token),
        }
        self.update_token(new_token, save=True)
        return True

    def update_refresh_token(self, token: str):
        self.token["refresh_token"] = token
        self.save()


def extract_exp(token: str) -> float:
    import jwt

    decoded = jwt.decode(token, options={"verify_signature": False})
    return decoded["exp"]


cred = Credential()
