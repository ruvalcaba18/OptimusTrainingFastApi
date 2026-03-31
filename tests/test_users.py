import io
from fastapi import status


USER_PAYLOAD = {
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


class TestCreateUser:
    def test_create_success(self, client):
        resp = client.post("/api/v1/users/", json=USER_PAYLOAD)
        assert resp.status_code == status.HTTP_201_CREATED
        data = resp.json()
        assert data["user"]["email"] == USER_PAYLOAD["email"]
        assert "hashed_password" not in data["user"]
        assert data["user"]["is_active"] is True
        assert "access_token" in data["token"]

    def test_create_duplicate_email(self, client):
        client.post("/api/v1/users/", json=USER_PAYLOAD)
        resp = client.post("/api/v1/users/", json=USER_PAYLOAD)
        assert resp.status_code == status.HTTP_409_CONFLICT

    def test_create_invalid_email(self, client):
        resp = client.post("/api/v1/users/", json={**USER_PAYLOAD, "email": "not-an-email"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_short_password(self, client):
        resp = client.post("/api/v1/users/", json={**USER_PAYLOAD, "password": "123"})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_negative_age(self, client):
        resp = client.post("/api/v1/users/", json={**USER_PAYLOAD, "age": -1})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_negative_weight(self, client):
        resp = client.post("/api/v1/users/", json={**USER_PAYLOAD, "weight": 0})
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
        assert resp.json()["id"] == test_user.id

    def test_read_user_not_found(self, client, auth_headers):
        resp = client.get("/api/v1/users/99999", headers=auth_headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_list_users(self, client, auth_headers, test_user):
        resp = client.get("/api/v1/users/", headers=auth_headers)
        assert resp.status_code == status.HTTP_200_OK
        assert isinstance(resp.json(), list)
        assert len(resp.json()) >= 1


class TestUpdateUser:
    def test_update_own_profile(self, client, auth_headers, test_user):
        resp = client.put(
            f"/api/v1/users/{test_user.id}",
            json={"first_name": "Actualizado"},
            headers=auth_headers,
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["first_name"] == "Actualizado"

    def test_cannot_update_other_user(self, client, db, auth_headers):
        from app.models.user import User
        from app.core.security import get_password_hash
        other = User(
            email="other@optimus.com",
            hashed_password=get_password_hash("Passw0rd!"),
            first_name="Other",
            last_name="User",
            phone="+521234567891",
            age=30,
            weight=70.0,
            height=170.0,
            exercise_frequency="2x/week",
            training_type="cardio",
            is_active=True,
        )
        db.add(other)
        db.commit()
        db.refresh(other)
        resp = client.put(
            f"/api/v1/users/{other.id}",
            json={"first_name": "Hacked"},
            headers=auth_headers,
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN


class TestDeleteUser:
    def test_delete_own_user(self, client, db):
        from app.models.user import User
        from app.core.security import get_password_hash
        user = User(
            email="todelete@optimus.com",
            hashed_password=get_password_hash("Passw0rd!"),
            first_name="Del",
            last_name="Me",
            phone="+521234567892",
            age=22,
            weight=65.0,
            height=165.0,
            exercise_frequency="1x/week",
            training_type="casa",
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        login = client.post(
            "/api/v1/auth/login",
            json={"email": "todelete@optimus.com", "password": "Passw0rd!"},
        )
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        resp = client.delete(f"/api/v1/users/{user.id}", headers=headers)
        assert resp.status_code == status.HTTP_200_OK


class TestProfilePicture:
    def test_upload_valid_jpg(self, client, auth_headers, test_user):
        fake_image = io.BytesIO(b"\xff\xd8\xff\xe0" + b"\x00" * 100)
        resp = client.post(
            f"/api/v1/users/{test_user.id}/photo",
            files={"file": ("photo.jpg", fake_image, "image/jpeg")},
            headers=auth_headers,
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()["profile_picture_url"] is not None

    def test_upload_invalid_extension(self, client, auth_headers, test_user):
        fake_gif = io.BytesIO(b"GIF89a" + b"\x00" * 50)
        resp = client.post(
            f"/api/v1/users/{test_user.id}/photo",
            files={"file": ("photo.gif", fake_gif, "image/gif")},
            headers=auth_headers,
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_upload_other_user_photo_forbidden(self, client, db, auth_headers):
        from app.models.user import User
        from app.core.security import get_password_hash
        other = User(
            email="photo_other@optimus.com",
            hashed_password=get_password_hash("Passw0rd!"),
            first_name="Photo",
            last_name="Other",
            phone="+521234567893",
            age=28,
            weight=72.0,
            height=172.0,
            exercise_frequency="4x/week",
            training_type="gimnasio",
            is_active=True,
        )
        db.add(other)
        db.commit()
        db.refresh(other)
        fake = io.BytesIO(b"\xff\xd8\xff\xe0" + b"\x00" * 100)
        resp = client.post(
            f"/api/v1/users/{other.id}/photo",
            files={"file": ("photo.jpg", fake, "image/jpeg")},
            headers=auth_headers,
        )
        assert resp.status_code == status.HTTP_403_FORBIDDEN
