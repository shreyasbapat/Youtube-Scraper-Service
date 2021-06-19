from uuid import uuid4
from http import HTTPStatus

import requests
from flask import Blueprint
from shuttlis.serialization import serialize
from voluptuous import Schema

from youtube.domain.models import Video
from youtube.store.repos import VideoRepo
from youtube.utils.flask import APISuccess, APIResponse, APIError
from youtube.utils.schema import dataschema
from youtube.utils.misc import parse_timestamp
from youtube.exapi.youtube import get_yt_service

blueprint = Blueprint("videos", __name__)


@blueprint.route("/")
def hello() -> APISuccess:
    # this adds all the fields specified inside the extra dict as attributes to the
    # logRecord object __dict__ for this log line
    res = requests.get("http://www.google.com")
    return APISuccess({"hello": "world"})


@blueprint.route("/health")
def health() -> APISuccess:
    return APISuccess({"data": "healthy"})


@blueprint.route("/videos", methods=["POST"])
@dataschema(
    Schema(
        {
            "id": str,
            "title": str,
            "description": str,
            "thumbnail": str,
            "published_at": str,
        }
    )
)
def create_video(
    id: str, title: str, description: str, thumbnail: str, published_at: str
) -> APISuccess:
    dt = parse_timestamp(published_at)
    video = Video(
        id=id,
        title=title,
        description=description,
        thumbnail=thumbnail,
        published_at=dt,
    )
    video = VideoRepo().create(video)

    return APISuccess(serialize(video))


@blueprint.route("/videos", methods=["GET"])
def fetch_videos() -> APISuccess:
    videos = VideoRepo().get_all()

    return APISuccess({"videos": serialize(videos)})


@blueprint.route("/videos/len", methods=["GET"])
def fetch_len_videos() -> APISuccess:
    videos = VideoRepo().get_all()

    return APISuccess({"videos": serialize(len(videos))})


@blueprint.route("/videos/<id>", methods=["GET"])
def get_video(id: str) -> APIResponse:
    video = VideoRepo().get(id)
    if not video:
        return APIError(
            error_type="NOT_FOUND",
            error_message="User not found",
            status=HTTPStatus.NOT_FOUND,
        )

    return APISuccess(serialize(video))


@blueprint.route("/videos/auto", methods=["GET"])
def push_videos() -> APIResponse:
    yts = get_yt_service()
    videos = yts.fetch_latest_videos()
    for video in videos:
        if not VideoRepo().get(video.id):
            VideoRepo().create(video=video)
    return APISuccess(serialize(videos))


@blueprint.route("/videos/clean", methods=["DELETE"])
def clean_videos() -> APIResponse:
    VideoRepo().flush()
    return APISuccess()
