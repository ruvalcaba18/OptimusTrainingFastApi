"""
Tests for user endpoints — CRUD + photo upload.
"""
import io
from fastapi import status


class TestCreateUser:
    PAYLOAD = {
        "email": "nuevo@optimus.com",
        "password": "Passw0rd!",
        "first_name": "Jael",
        "last_name": "Ruvalcaba",
        "phone": "+521234567890",
        "age": 28,
        "weight": 80.0,
        "height": 178.0,
        "exercise_frequency": "5x/week",
        "training_type": "gimnasio",
    }

    def test_create_user_success(self, client):
        resp = client.post("/api/v1/users/", json=self.PAYLOAD)
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.json()
        assert data["email"] == self.PAYLOAD["email"]
        assert "hashed_password" not in data
        assert data["is_active"] is True

    def test_create_user_duplicate_email(self, client):
        client.post("/api/v1/users/", json=self.PAYLOAD)
        resp = client.post("/api/v1/users/", json=self.PAYLOAD)
        assert resp.status_code == status.HTTP_409_CONFLICT

    def test_create_user_invalid_email(self, client):
        payload = {**self.PAYLOAD, "email": "not-an-email"}
        resp = client.post("/api/v1/users/", json=payload)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_short_password(self, client):
        payload = {**self.PAYLOAD, "password": "123"}
        resp = client.post("/api/v1/users/", json=payload)
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestReadUsers:
    def test_read_me(self, client, auth_headers):
        resp = client.get("/api/v1/users/me", headers=auth_headers)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["email"] == "testuser@optimus.com"

    def test_read_me_unauthenticated(self, client):
        resp = client.get("/api/v1/users/me")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_read_user_by_id(self, client, auth_headers, test_user):
        resp = client.get(f"/api/v1/users/{test_user.id}", headers=auth_headers)
        assert resp.status_code == status.HTTP_200_OK

    def test_read_user_not_found(self, client, auth_headers):
        resp = client.get("/api/v1/users/99999", headers=auth_headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateUser:
    def test_update_own_user(self, client, auth_headers, test_user):
        resp = client.put(
            f"/api/v1/users/{test_user.id}",
            json={"first_name": "Updated"},
            headers=auth_headers,
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["first_name"] == "Updated"


class TestProfilePicture:
    def test_upload_profile_picture(self, client, auth_headers, test_user):
        # Create a minimal valid JPEG in-memory
        fake_image = io.BytesIO(b"\xff\xd8\xff\xe0" + b"\x00" * 100)
        fake_image.name = "photo.jpg"
        resp = client.post(
            f"/api/v1/users/{test_user.id}/photo",
            files={"file": ("photo.jpg", fake_image, "image/jpeg")},
            headers=auth_headers,
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["profile_picture_url"] is not None
        assert "profile_pictures" in resp.json()["profile_picture_url"]

    def test_upload_invalid_extension(self, client, auth_headers, test_user):
        fake_gif = io.BytesIO(b"GIF89a" + b"\x00" * 50)
        resp = client.post(
            f"/api/v1/users/{test_user.id}/photo",
            files={"file": ("photo.gif", fake_gif, "image/gif")},
            headers=auth_headers,
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
