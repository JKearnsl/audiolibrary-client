import hashlib
import logging
import pickle
from enum import Enum

import httpx

from audiolibrary.api_service import APIServiceV1, ErrorModel, ErrorType
from audiolibrary.models.base import BaseModel


def get_http_session() -> httpx.Client:
    session = httpx.Client()
    try:
        cookies = httpx.Cookies()
        with open("session", "rb") as file:
            jar_cookies = pickle.load(file)
        for domain, pc in jar_cookies.items():
            for path, c in pc.items():
                for k, v in c.items():
                    cookies.set(k, v.value, domain=domain, path=path)
        session.cookies = cookies
    except (FileNotFoundError, EOFError):
        logging.info(" Файл сессии не найден")
    return session


class LoginModel(BaseModel):

    def __init__(self, base_url: str):
        super().__init__()
        self.api_service = APIServiceV1(base_url, get_http_session())

    def is_auth(self) -> bool:
        if self.api_service.current_user().get("error"):
            self.api_service.session.cookies.clear()
            return False
        return True

    def signin(self, username: str, password: str) -> bool:
        result = self.api_service.signin(username, password)
        if result.get("error"):
            self.raise_error(ErrorModel(result["error"]["content"], result["error"]["type"]))
            return False

        with open("session", "wb") as file:
            # Issues: https://github.com/encode/httpx/issues/895#issuecomment-970689380
            pickle.dump(self.api_service.session.cookies.jar.__getattribute__("_cookies"), file)
        return True

    def signup(self, username: str, password: str, repeat_password: str) -> bool:
        if password != repeat_password:
            self.raise_error(ErrorModel("Пароли не совпадают", ErrorType.MESSAGE))
            return False

        result = self.api_service.signup(username, password)
        if result.get("error"):
            self.raise_error(ErrorModel(result["error"]["content"], result["error"]["type"]))
            return False
        return True
