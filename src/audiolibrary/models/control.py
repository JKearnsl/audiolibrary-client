from audiolibrary.config import InIConfig
from audiolibrary.models import MenuItem
from audiolibrary.models.base import BaseModel


class ControlModel(BaseModel):
    id: MenuItem = MenuItem.CONTROL

    def __init__(self):
        super().__init__()
