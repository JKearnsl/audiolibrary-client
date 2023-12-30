from enum import Enum

import psutil

from audiolibrary.api_service import APIServiceV1
from audiolibrary.models.base import BaseModel


class MenuItem(str, Enum):
    BROWSE: str = "browse"
    LIKED: str = "liked"
    POPULAR: str = "popular"
    CONTROL: str = "control"
    UPLOAD: str = "upload"


class MainModel(BaseModel):

    def __init__(self, api_service: APIServiceV1, **scope):
        super().__init__()
        self.is_debug = scope["is_debug"]
        self.is_auth = api_service.is_auth
        self.app_title = scope["app_title"]
        self.app_version = scope["app_version"]
        self.contact = scope["contact"]
        self.scope = scope

        self.api_service = api_service

    @staticmethod
    def get_ram_usage() -> int:
        return int(psutil.Process().memory_info().rss / (1024 * 1024))

    def get_current_user(self):
        result = self.api_service.current_user()
        if result.get("error") is None:
            return result.get("content")

        self.raise_error(result.get("error"))
