import psutil

from audiolibrary.config import InIConfig, Contact
from audiolibrary.models.base import BaseModel

from enum import Enum


class MenuItem(str, Enum):
    BROWSE: str = "browse"
    LIKED: str = "liked"
    POPULAR: str = "popular"
    CONTROL: str = "control"
    UPLOAD: str = "upload"


class MainModel(BaseModel):

    def __init__(self, is_debug: bool, app_title: str, app_version: str, contact: Contact):
        super().__init__()
        self.is_debug = is_debug
        self.app_title = app_title
        self.app_version = app_version
        self.contact = contact

    @staticmethod
    def get_ram_usage() -> int:
        return int(psutil.Process().memory_info().rss / (1024 * 1024))
