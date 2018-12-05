from pytest import fixture
from eio_userdb.main import app
from eio_userdb.model import init_db

@fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['TESTING'] = True
    client = app.test_client()
    init_db()

    return client
