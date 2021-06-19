from dataclasses import dataclass
from datetime import datetime


@dataclass
class Video:
    id: str
    title: str
    description: str
    published_at: datetime
    thumbnail: str
