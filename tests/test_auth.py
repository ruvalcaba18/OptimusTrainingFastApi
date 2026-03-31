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
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_access_token_form(self, client, test_user):
        resp = client.post(
            "/api/v1/auth/login/access-token",
            data={"username": "testuser@optimus.com", "password": "Passw0rd!"},
        )
        assert resp.status_code == status.HTTP_200_OK
        assert "access_token" in resp.json()

    def test_login_wrong_password(self, client, test_user):
        resp = client.post(
            "/api/v1/auth/login",
            json={"email": "testuser@optimus.com", "password": "wrongpass"},
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, client):
        resp = client.post(
            "/api/v1/auth/login",
            json={"email": "ghost@optimus.com", "password": "Passw0rd!"},
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_missing_password(self, client):
        resp = client.post("/api/v1/auth/login", json={"email": "only@email.com"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_missing_email(self, client):
        resp = client.post("/api/v1/auth/login", json={"password": "Passw0rd!"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestRefreshToken:
    def test_refresh_token_success(self, client, test_user):
        login = client.post(
            "/api/v1/auth/login",
            json={"email": "testuser@optimus.com", "password": "Passw0rd!"},
        )
        refresh_token = login.json()["refresh_token"]
        resp = client.post(
            "/api/v1/auth/refresh-token",
            params={"refresh_token": refresh_token},
        )
        assert resp.status_code == status.HTTP_200_OK
        assert "access_token" in resp.json()

    def test_refresh_token_invalid(self, client):
        resp = client.post(
            "/api/v1/auth/refresh-token",
            params={"refresh_token": "not.a.valid.token"},
        )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
