import os
import tempfile

import pytest
from groceries import create_app
from groceries.db import get_db, init_db, close_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    app = create_app({ 'TESTING': True})

    with app.app_context():
        init_db()
        connection = get_db()
        connection.cursor().execute(_data_sql)
        connection.commit()
        yield app
        close_db()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def db(app):
    return get_db().cursor()

