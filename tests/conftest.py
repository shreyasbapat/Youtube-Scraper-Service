import logging

import pytest

from youtube import create_app


@pytest.fixture
def app():
    app = create_app()
    app.testing = True

    from youtube.store import db

    with app.app_context():
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
            db.session.commit()

        # By using a yield statement instead of return, all the code after the
        # yield statement serves as the teardown code:
        # https://docs.pytest.org/en/latest/fixture.html#fixture-finalization-executing-teardown-code
        yield app
