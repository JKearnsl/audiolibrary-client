from audiolibrary.config import InIConfig
from audiolibrary.models import MenuItem
from audiolibrary.models.base import BaseModel


class BrowseModel(BaseModel):
    id: MenuItem = MenuItem.BROWSE

    def __init__(self, theme: tuple[type[any], str, str], config: InIConfig):
        super().__init__(theme)
        self.config = config
