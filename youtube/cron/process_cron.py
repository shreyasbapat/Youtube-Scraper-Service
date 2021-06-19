from youtube import create_app
from youtube.exapi.youtube import get_yt_service
from youtube.store.repos import VideoRepo

flask_app = create_app()


def process_videos():
    yts = get_yt_service()
    videos = yts.fetch_latest_videos()
    for video in videos:
        if not VideoRepo().get(video.id):
            VideoRepo().create(video=video)


if __name__ == "__main__":
    with flask_app.app_context():
        try:
            process_videos()
        except Exception as e:
            raise e
