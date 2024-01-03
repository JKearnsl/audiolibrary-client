from pydantic import BaseModel


class Music(BaseModel):
    id: int
    title: str
    artist: str
    album: str
    duration: int
    cover_url: str
