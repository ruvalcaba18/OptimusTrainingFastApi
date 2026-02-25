"""
Tests for auth endpoints.
"""
from fastapi import status


class TestLogin:
    def test_login_success(self, client, test_user):
        resp = client.post(
            "/api/v1/auth/login",
            json={"email": "testuser@optimus.com", "password": "Passw0rd!"},
        )
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_access_token_success(self, client, test_user):
        resp = client.post(
            "/api/v1/auth/login/access-token",
            data={"username": "testuser@optimus.com", "password": "Passw0rd!"},
        )
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user):
        resp = client.post(
            "/api/v1/auth/login",
            json={"email": "testuser@optimus.com", "password": "wrong"},
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, client):
        resp = client.post(
            "/api/v1/auth/login",
            json={"email": "ghost@optimus.com", "password": "Passw0rd!"},
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_missing_fields(self, client):
        resp = client.post("/api/v1/auth/login", json={"email": "only@email.com"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
