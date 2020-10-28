import pytest
import os
from pathlib import Path

from project.app import app, init_db

TEST_DB = "test.db"

@pytest.fixture
def client():
    BASE_DIR = Path(__file__).resolve().parent.parent
    app.config['TESTING'] = True
    app.config['DATABASE'] = BASE_DIR.joinpath(TEST_DB)

    init_db() #setup
    yield app.test_client() #tests get run here
    init_db() #teardown

def login(client, username, password):
    """ Login helper"""
    return client.post(
        "/login",
        data=dict(username=username, password=password),
        follow_redirects=True,
    )

def logout(client):
    """ Logout helper """
    return client.get("/logout", follow_redirects=True)

#testing that the basic index page works
def test_index():
    tester = app.test_client()
    response = tester.get('/', content_type='html/text')

    assert response.status_code == 200


#testing that a database file exists
def test_database():
    init_db()
    assert Path("flaskr.db").is_file()

def test_empty_db(client):
    """Ensure database is blank"""
    rv = client.get("/")
    assert b"No entries yet. Add some!" in rv.data

def test_login_logout(client):
    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"])
    assert b"You were logged in" in rv.data
    rv = logout(client)
    assert b"You were logged out" in rv.data
    rv = login(client, app.config["USERNAME"]+"x", app.config["PASSWORD"])
    assert b"Invalid username" in rv.data
    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"]+'x')
    assert b"Invalid password" in rv.data

def test_messages(client):
    login(client, app.config['USERNAME'], app.config['PASSWORD'])
    rv = CLIENT.POST(
        "/add",
        data=dict(title="<Hello>", text="<string>HTML</strong> allowed here"),
        follow_redirects=True,
    )
    assert b"No entries here so far" not in rv.data
    assert b"&lt;Hello&gt;" in rv.data   
    assert b"<strong>HTML</strong> allowed here" in rv.data   
