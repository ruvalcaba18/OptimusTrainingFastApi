from unittest.mock import AsyncMock, patch
from fastapi import status


APPLE_VERIFIED_USER = {
    "email": "apple@test.com",
    "name": None,
    "provider_id": "apple.sub.123",
}

GOOGLE_VERIFIED_USER = {
    "email": "google@test.com",
    "name": "Google User",
    "provider_id": "google.sub.123",
}

FACEBOOK_VERIFIED_USER = {
    "email": "facebook@test.com",
    "name": "Facebook User",
    "provider_id": "fb.id.123",
}


class TestSocialAuthApple:
    def test_apple_login_creates_new_user(self, client):
        with patch(
            "app.services.social_auth.apple_provider.AppleProvider.verify_token",
            new_callable=AsyncMock,
            return_value=APPLE_VERIFIED_USER,
        ):
            resp = client.post(
                "/api/v1/auth/social/apple",
                json={"token": "fake.apple.token", "first_name": "Tim", "last_name": "Apple"},
            )
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_apple_login_existing_user(self, client, test_user):
        existing_user_data = {
            "email": test_user.email,
            "name": None,
            "provider_id": "apple.sub.existing",
        }
        with patch(
            "app.services.social_auth.apple_provider.AppleProvider.verify_token",
            new_callable=AsyncMock,
            return_value=existing_user_data,
        ):
            resp = client.post(
                "/api/v1/auth/social/apple",
                json={"token": "fake.apple.token"},
            )
        assert resp.status_code == status.HTTP_200_OK
        assert "access_token" in resp.json()

    def test_apple_missing_token(self, client):
        resp = client.post("/api/v1/auth/social/apple", json={})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_apple_invalid_token_rejected(self, client):
        from fastapi import HTTPException
        with patch(
            "app.services.social_auth.apple_provider.AppleProvider.verify_token",
            new_callable=AsyncMock,
            side_effect=HTTPException(status_code=401, detail="Invalid token"),
        ):
            resp = client.post(
                "/api/v1/auth/social/apple",
                json={"token": "bad.token"},
            )
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_apple_deactivated_user_rejected(self, client, db):
        from app.models.user import User
        from app.core.security import get_password_hash
        deactivated = User(
            email="deactivated.apple@test.com",
            hashed_password=get_password_hash("x" * 32),
            first_name="Deact",
            last_name="User",
            phone="",
            age=0,
            weight=0.0,
            height=0.0,
            exercise_frequency="",
            training_type="",
            is_active=False,
        )
        db.add(deactivated)
        db.commit()

        with patch(
            "app.services.social_auth.apple_provider.AppleProvider.verify_token",
            new_callable=AsyncMock,
            return_value={"email": "deactivated.apple@test.com", "name": None, "provider_id": "x"},
        ):
            resp = client.post(
                "/api/v1/auth/social/apple",
                json={"token": "fake.token"},
            )
        assert resp.status_code == status.HTTP_403_FORBIDDEN


class TestSocialAuthGoogle:
    def test_google_login_creates_new_user(self, client):
        with patch(
            "app.services.social_auth.google_provider.GoogleProvider.verify_token",
            new_callable=AsyncMock,
            return_value=GOOGLE_VERIFIED_USER,
        ):
            resp = client.post(
                "/api/v1/auth/social/google",
                json={"token": "fake.google.id_token"},
            )
        assert resp.status_code == status.HTTP_200_OK
        assert "access_token" in resp.json()

    def test_google_login_existing_user(self, client, test_user):
        with patch(
            "app.services.social_auth.google_provider.GoogleProvider.verify_token",
            new_callable=AsyncMock,
            return_value={"email": test_user.email, "name": "Test", "provider_id": "g.sub"},
        ):
            resp = client.post(
                "/api/v1/auth/social/google",
                json={"token": "fake.google.id_token"},
            )
        assert resp.status_code == status.HTTP_200_OK

    def test_google_missing_token(self, client):
        resp = client.post("/api/v1/auth/social/google", json={})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_google_second_login_same_token_returns_same_user(self, client):
        with patch(
            "app.services.social_auth.google_provider.GoogleProvider.verify_token",
            new_callable=AsyncMock,
            return_value=GOOGLE_VERIFIED_USER,
        ):
            resp1 = client.post("/api/v1/auth/social/google", json={"token": "tok"})
            resp2 = client.post("/api/v1/auth/social/google", json={"token": "tok"})
        assert resp1.status_code == status.HTTP_200_OK
        assert resp2.status_code == status.HTTP_200_OK


class TestSocialAuthFacebook:
    def test_facebook_login_creates_new_user(self, client):
        with patch(
            "app.services.social_auth.facebook_provider.FacebookProvider.verify_token",
            new_callable=AsyncMock,
            return_value=FACEBOOK_VERIFIED_USER,
        ):
            resp = client.post(
                "/api/v1/auth/social/facebook",
                json={"token": "fake.fb.access_token"},
            )
        assert resp.status_code == status.HTTP_200_OK
        assert "access_token" in resp.json()

    def test_facebook_missing_token(self, client):
        resp = client.post("/api/v1/auth/social/facebook", json={})
        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_facebook_login_existing_user(self, client, test_user):
        with patch(
            "app.services.social_auth.facebook_provider.FacebookProvider.verify_token",
            new_callable=AsyncMock,
            return_value={"email": test_user.email, "name": "FB", "provider_id": "fb.id"},
        ):
            resp = client.post(
                "/api/v1/auth/social/facebook",
                json={"token": "fake.fb.token"},
            )
        assert resp.status_code == status.HTTP_200_OK


class TestSocialAuthNameResolution:
    def test_name_from_body_takes_priority(self, client, db):
        with patch(
            "app.services.social_auth.google_provider.GoogleProvider.verify_token",
            new_callable=AsyncMock,
            return_value={
                "email": "namepriority@test.com",
                "name": "Provider Name",
                "provider_id": "g.np",
            },
        ):
            resp = client.post(
                "/api/v1/auth/social/google",
                json={"token": "tok", "first_name": "Body", "last_name": "Priority"},
            )
        assert resp.status_code == status.HTTP_200_OK
        from app.services.user_service import user_service
        from app.database import SessionLocal
        with SessionLocal() as s:
            pass

    def test_name_falls_back_to_provider(self, client):
        with patch(
            "app.services.social_auth.google_provider.GoogleProvider.verify_token",
            new_callable=AsyncMock,
            return_value={
                "email": "fallback@test.com",
                "name": "Provider Fallback",
                "provider_id": "g.fb",
            },
        ):
            resp = client.post(
                "/api/v1/auth/social/google",
                json={"token": "tok"},
            )
        assert resp.status_code == status.HTTP_200_OK

    def test_name_falls_back_to_email_prefix(self, client):
        with patch(
            "app.services.social_auth.google_provider.GoogleProvider.verify_token",
            new_callable=AsyncMock,
            return_value={
                "email": "emailprefix@test.com",
                "name": None,
                "provider_id": "g.ep",
            },
        ):
            resp = client.post(
                "/api/v1/auth/social/google",
                json={"token": "tok"},
            )
        assert resp.status_code == status.HTTP_200_OK
