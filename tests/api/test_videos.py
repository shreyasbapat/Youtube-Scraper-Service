from http import HTTPStatus

import pytest

from youtube.utils.flask import APIFlask


@pytest.mark.integration
def test_hello_world_is_returned(app: APIFlask):
    with app.test_client() as client:
        response = client.get("/")
        data = response.get_json()["data"]
        assert HTTPStatus.OK == response.status_code
        assert "world" == data["hello"]


@pytest.mark.integration
def test_create_and_fetch_video(app: APIFlask):
    with app.test_client() as client:
        response = client.post(
            "/videos",
            json={
                "id": "7ipO9f0905Y",
                "title": "Giannis on WINNING Game 7 & Advancing to Conference Finals! | Postgame Press Conference",
                "description": "Subscribe to the NBA: https://on.nba.com/2JX5gSN\n\nFull Game Highlights Playlist: https://on.nba.com/2rjGMge\n\nFor news, stories, highlights and more, go to our official website at https://app.link.nba.com/e/NBA_site\n\nGet NBA LEAGUE PASS: https://nba.app.link/nbaleaguepass5",
                "thumbnail": "https://i.ytimg.com/vi/7ipO9c0905Y/default.jpg",
                "published_at": "2021-06-20T04:46:31Z",
            },
        )
        assert HTTPStatus.OK == response.status_code

    video_id = response.get_json()["data"]["id"]

    with app.test_client() as client:
        response = client.get("/videos/%s" % video_id)
        assert HTTPStatus.OK == response.status_code

    name = response.get_json()["data"]["title"]
    assert "Giannis" in name


@pytest.mark.integration
def test_fetch_videos(app: APIFlask):
    with app.test_client() as client:
        response = client.post(
            "/videos",
            json={
                "id": "7ipO9f0905Y",
                "title": "Giannis on WINNING Game 7 & Advancing to Conference Finals! | Postgame Press Conference",
                "description": "Subscribe to the NBA: https://on.nba.com/2JX5gSN\n\nFull Game Highlights Playlist: https://on.nba.com/2rjGMge\n\nFor news, stories, highlights and more, go to our official website at https://app.link.nba.com/e/NBA_site\n\nGet NBA LEAGUE PASS: https://nba.app.link/nbaleaguepass5",
                "thumbnail": "https://i.ytimg.com/vi/7ipO9c0905Y/default.jpg",
                "published_at": "2021-06-20T04:46:31Z",
            },
        )
        assert HTTPStatus.OK == response.status_code

    with app.test_client() as client:
        response = client.get("/videos")
        assert HTTPStatus.OK == response.status_code

    l = response.get_json()["data"]["videos"]

    assert len(l) == 1


@pytest.mark.integration
def test_fetch_videos(app: APIFlask):
    with app.test_client() as client:
        response = client.get("/videos/auto",)
        assert HTTPStatus.OK == response.status_code

    with app.test_client() as client:
        response = client.get("/videos")
        assert HTTPStatus.OK == response.status_code

    l = response.get_json()["data"]["videos"]

    assert len(l) == 50


@pytest.mark.integration
def test_fetch_videos(app: APIFlask):
    with app.test_client() as client:
        response = client.get("/videos/auto",)
        assert HTTPStatus.OK == response.status_code
    with app.test_client() as client:
        response = client.get("/api/v1/youtube/videos", query_string={"page": 1, "query": "Live"})

    l = response.get_json()["data"]["videos"]

    assert len(l) <= 10
