from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_get_weather():
    response = client.get("/weather?city=Seoul")
    assert response.status_code == 200
    assert response.json() == {"message": "You asked for weather in Seoul!"}
