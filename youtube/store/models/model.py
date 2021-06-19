from youtube.store import db

from sqlalchemy import func


class VideoModel(db.Model):
    __tablename__ = "youtube_vids"

    id = db.Column(db.String(11), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    title = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    thumbnail = db.Column(db.Text(), nullable=False)
    published_at = db.Column(db.DateTime, nullable=False, default=func.now())
