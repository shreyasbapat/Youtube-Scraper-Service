import requests
from datetime import datetime, timedelta

from http import HTTPStatus
from typing import List

from youtube import Config
from youtube.domain.models import Video


def _get_dt():
    dt = datetime.utcnow() - timedelta(days=10)
    return dt.isoformat().split("+")[0] + "Z"


def _to_yt(data, index=0):
    return Video(
        id=data[index]["id"]["videoId"],
        title=data[index]["snippet"]["title"],
        description=data[index]["snippet"]["description"],
        thumbnail=data[index]["snippet"]["thumbnails"]["default"]["url"],
        published_at=data[index]["snippet"]["publishedAt"],
    )


def _to_yts(videos):
    return [
        Video(
            id=video["id"]["videoId"],
            title=video["snippet"]["title"],
            description=video["snippet"]["description"],
            thumbnail=video["snippet"]["thumbnails"]["default"]["url"],
            published_at=video["snippet"]["publishedAt"],
        )
        for video in videos
    ]


class YTDataService:
    def __init__(self, key):
        self.key = key
        self.url = "https://www.googleapis.com/youtube/v3"
        self.session = requests.Session()

    def fetch_video(self, id) -> Video:
        url = f"{self.url}/videos"
        params = {"key": self.key, "id": id, "part": "snippet"}
        response = self.session.get(url, params=params)

        if response.status_code == HTTPStatus.OK:
            return _to_yt(response.json()["items"])

        raise _mk_exc(response)

    def fetch_latest_videos(self) -> List[Video]:
        url = f"{self.url}/search"
        params = {
            "key": self.key,
            "type": "video",
            "order": "date",
            "maxResults": 50,
            "q": Config.QUERY,
            "part": "snippet",
            "publishedAfter": _get_dt(),
        }
        response = self.session.get(url, params=params)

        if response.status_code == HTTPStatus.OK:
            return _to_yts(response.json()["items"])

        raise _mk_exc(response)


class YTDataError(Exception):
    pass


def _mk_exc(response):
    return YTDataError(
        f"""
        Invalid response from youtube.
        Status code: {response.status_code}.
        Body: {response.text}
        """
    )


def get_yt_service():
    return YTDataService(Config.YOUTUBE_API_KEY)
