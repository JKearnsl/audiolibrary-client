import psutil

from audiolibrary.config import InIConfig
from audiolibrary.models.base import BaseModel

from enum import Enum


class MenuItem(str, Enum):
    BROWSE: str = "browse"
    LIKED: str = "liked"
    POPULAR: str = "popular"
    CONTROL: str = "control"
    UPLOAD: str = "upload"


class MainModel(BaseModel):

    def __init__(self, theme: tuple[type[any], str, str], config: InIConfig):
        super().__init__(theme)
        self.config = config

    @staticmethod
    def get_ram_usage() -> int:
        return int(psutil.Process().memory_info().rss / (1024 * 1024))
