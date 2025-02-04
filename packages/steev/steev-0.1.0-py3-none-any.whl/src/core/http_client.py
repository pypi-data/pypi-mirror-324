import requests

from src.urls.run import RunURL
from src.utils.credentials import Credential, cred


class Client:
    def __init__(self, cred: Credential):
        self.cred = cred

    def send_code(self, code: str, params: dict, steev_cfg: dict):
        response = requests.post(
            RunURL.register_train,
            json={
                "train_code": code,
                "user_parameters": params,
                "steev_cfg": steev_cfg,
            },
            headers=self._prepare_auth_header(),
        )

        if response.status_code == 201:
            return response.json()
        elif response.status_code == 401:
            raise UnAuthorizedException
        else:
            raise Exception(response.text)

    def _prepare_auth_header(self):
        return {"Authorization": f"Bearer {self.cred.token['access_token']}"}


class UnAuthorizedException(Exception):
    pass


client = Client(cred)
