from audiolibrary.config import InIConfig
from audiolibrary.models import MenuItem
from audiolibrary.models.base import BaseModel


class LikedModel(BaseModel):
    id: MenuItem = MenuItem.LIKED

    def __init__(self):
        super().__init__()
