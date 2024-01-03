from audiolibrary.config import InIConfig
from audiolibrary.models import MenuItem
from audiolibrary.models.base import BaseModel
from audiolibrary.models.schemas.music import Music


class BrowseModel(BaseModel):
    id: MenuItem = MenuItem.BROWSE

    def __init__(self):
        super().__init__()

    def search(self, query: str) -> list[Music]:
        return [
            Music(
                id=1,
                title="Moonlight Sonata",
                artist="Ludwig van Beethoven",
                album="Classical Music",
                duration=120,
                cover_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Beethoven.jpg/220px-Beethoven.jpg",
            ),
            Music(
                id=2,
                title="Sonata No. 14",
                artist="Ludwig van Beethoven",
                album="Classical Music",
                duration=60,
                cover_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Beethoven.jpg/220px-Beethoven.jpg",
            ),
            Music(
                id=3,
                title="Sonata No. 15",
                artist="Ludwig van Beethoven",
                album="Classical Music",
                duration=110,
                cover_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Beethoven.jpg/220px-Beethoven.jpg",
            ),

        ]
