
import os

import pytest
from flask import json
from microservice import create_app
from microservice.config import config_dict


@pytest.fixture
def client():
    DEBUG = (os.getenv('DEBUG', 'False') == 'True')
    get_config_mode = 'Debug' if DEBUG else 'Production'
    app_config = config_dict[get_config_mode.capitalize()]
    app = create_app(app_config)

    with app.test_client() as client:
        with app.app_context():
            print("Initialize test application")
        yield client

    # os.close(db_fd)
    # os.unlink(app.config['DATABASE'])


def test_index(client):
    r = client.get("/")
    assert r.status_code == 302
    assert "/api" in r.get_data(as_text=True)


def test_get_books(client):
    r = client.get("/api/books/")
    assert r.status_code == 200
    books = json.loads(r.data)
    assert len(books) == 2


def test_add_book(client):
    r = client.post("/api/books/", data=dict(
        title='title',
        author='author'
    ))
    assert r.status_code == 200
    book = json.loads(r.data)
    assert book['title'] == "title"
    assert book['author'] == "author"


def test_get_book(client):
    r = client.get("/api/books/2")
    assert r.status_code == 200
    book = json.loads(r.data)
    assert book['title'] == "title"
    assert book['author'] == "author"


def test_update_book(client):
    r = client.post("/api/books/2", data={"key": "ISBN", "value": "1234"})
    assert r.status_code == 200
    book = json.loads(r.data)
    assert book['title'] == "title"
    assert book['author'] == "author"
    assert book['details'][0]["key"] == "ISBN"
    assert book['details'][0]["value"] == "1234"
