from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_login_success():
    response = client.post(
        "/api/login",
        json={"username": "admin", "password": "secret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "login success"
    assert "token" in data


def test_api_login_invalid_credentials():
    response = client.post(
        "/api/login",
        json={"username": "admin", "password": "wrongpass"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "invalid credentials"


def test_api_login_invalid_input():
    response = client.post(
        "/api/login",
        json={"username": "", "password": ""},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "invalid input"
