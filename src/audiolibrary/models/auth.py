import hashlib
import logging
import pickle
from enum import Enum

import httpx

from audiolibrary.api_service import APIServiceV1, ErrorModel, ErrorType
from audiolibrary.models.base import BaseModel


class AuthModel(BaseModel):

    def __init__(self, api_service: APIServiceV1):
        super().__init__()
        self.api_service = api_service

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
