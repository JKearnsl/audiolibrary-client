from audiolibrary.models import MenuItem
from audiolibrary.models.base import BaseModel


class UploadModel(BaseModel):
    id: MenuItem = MenuItem.UPLOAD

    def __init__(self):
        super().__init__()
