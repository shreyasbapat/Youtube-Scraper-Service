from flask import Blueprint
from shuttlis.serialization import serialize
from voluptuous import Schema, Coerce

from youtube.store.repos import VideoRepo
from youtube.utils.flask import APISuccess, APIResponse, APIError
from youtube.utils.schema import queryschema
from flask_paginate import Pagination

blueprint = Blueprint("youtube", __name__, url_prefix="/api/v1/youtube")


def get_videos(videos, offset=0, per_page=10):
    return videos[offset : offset + per_page]


@blueprint.route("/videos", methods=["GET"])
@queryschema(Schema({"page": Coerce(int), "query": Coerce(str)}))
def fetch_paginated_videos(page, query) -> APISuccess:
    videos = VideoRepo().get_query(query)
    per_page = 10
    offset = (page - 1) * per_page
    total = len(videos)
    if page >= total or page < 1:
        return APIError(error_type="PAGE_INVALID")
    pagination_videos = get_videos(videos=videos, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total)

    return APISuccess(
        {
            "videos": serialize(
                {
                    "page": page,
                    "per_page": per_page,
                    "pagination": pagination,
                    "videos": pagination_videos,
                }
            )
        }
    )
