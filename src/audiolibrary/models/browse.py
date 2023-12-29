from audiolibrary.config import InIConfig
from audiolibrary.models import MenuItem
from audiolibrary.models.base import BaseModel


class BrowseModel(BaseModel):
    id: MenuItem = MenuItem.BROWSE

    def __init__(self):
        super().__init__()
