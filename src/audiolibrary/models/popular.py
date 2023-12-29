from audiolibrary.config import InIConfig
from audiolibrary.models import MenuItem
from audiolibrary.models.base import BaseModel


class PopularModel(BaseModel):
    id: MenuItem = MenuItem.POPULAR

    def __init__(self):
        super().__init__()
