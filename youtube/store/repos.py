from typing import List, Optional
from youtube.store import db

from youtube.domain.models import Video
from youtube.store.models.model import VideoModel


class VideoRepo:
    def create(self, video: Video) -> Video:
        video_model = VideoModel(
            id=video.id,
            title=video.title,
            description=video.description,
            thumbnail=video.thumbnail,
            published_at=video.published_at,
        )
        db.session.add(video_model)
        db.session.commit()

        return self.get(video.id)

    def flush(self):
        db.session.query(VideoModel).delete()
        db.session.commit()
        return

    def get(self, video_id: str) -> Optional[Video]:
        video_model = db.session.query(VideoModel).get(video_id)
        if not video_model:
            return None

        return Video(
            id=video_model.id,
            title=video_model.title,
            description=video_model.description,
            thumbnail=video_model.thumbnail,
            published_at=video_model.published_at,
        )

    def get_all(self) -> List[Video]:
        video_models = (
            db.session.query(VideoModel)
                .order_by(VideoModel.published_at.desc())
                .all()
        )
        return [
            Video(
                id=video_model.id,
                title=video_model.title,
                description=video_model.description,
                thumbnail=video_model.thumbnail,
                published_at=video_model.published_at,
            )
            for video_model in video_models
        ]

    def get_query(self, q) -> List[Video]:
        video_models = (
            db.session.query(VideoModel)
            .filter(
                VideoModel.title.ilike(f'%{q}%') | VideoModel.description.ilike(f'%{q}%')
            )
            .order_by(VideoModel.published_at.desc())
            .all()
        )
        return [
            Video(
                id=video_model.id,
                title=video_model.title,
                description=video_model.description,
                thumbnail=video_model.thumbnail,
                published_at=video_model.published_at,
            )
            for video_model in video_models
        ]
