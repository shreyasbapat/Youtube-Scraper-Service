from os import getenv

from youtube.store import configure_db_with_app
from youtube.utils.config import Config
from youtube.utils.consul_patch import requests_use_srv_records

# local imports
from youtube.utils.flask import APIFlask


def create_app() -> APIFlask:
    app = APIFlask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # NOTE: Order matters here
    configure_db_with_app(app)
    _register_all_blueprints(app)

    requests_use_srv_records()

    return app


def _register_all_blueprints(app: APIFlask):
    from youtube.api.videos import blueprint as videos
    from youtube.api.youtube import blueprint as youtube

    app.register_blueprint(videos)
    app.register_blueprint(youtube)
