from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from fastapi import HTTPException

from app.core import security


class TestSecurityTokens:
    def test_access_token_is_string(self):
        token = security.create_access_token("user@test.com")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_refresh_token_is_string(self):
        token = security.create_refresh_token("user@test.com")
        assert isinstance(token, str)

    def test_password_reset_token_is_string(self):
        token = security.create_password_reset_token("user@test.com")
        assert isinstance(token, str)

    def test_verify_correct_password(self):
        hashed = security.get_password_hash("mypassword")
        assert security.verify_password("mypassword", hashed) is True

    def test_verify_wrong_password(self):
        hashed = security.get_password_hash("mypassword")
        assert security.verify_password("wrongpassword", hashed) is False

    def test_different_passwords_different_hashes(self):
        h1 = security.get_password_hash("pass1")
        h2 = security.get_password_hash("pass2")
        assert h1 != h2

    def test_same_password_different_hash_each_time(self):
        h1 = security.get_password_hash("samepass")
        h2 = security.get_password_hash("samepass")
        assert h1 != h2


class TestAppleProviderUnit:
    @pytest.mark.asyncio
    async def test_verify_token_missing_email_raises_401(self):
        from app.services.social_auth.apple_provider import AppleProvider
        from jose import jwt as jose_jwt

        mock_keys = [{"kid": "key1", "kty": "RSA"}]
        mock_payload = {"sub": "apple.user.123"}

        with patch.object(AppleProvider, "_fetch_apple_public_keys", new_callable=AsyncMock, return_value=mock_keys), \
             patch("app.services.social_auth.apple_provider.jwt.get_unverified_header", return_value={"kid": "key1"}), \
             patch("app.services.social_auth.apple_provider.jwt.decode", return_value=mock_payload):
            with pytest.raises(HTTPException) as exc_info:
                await AppleProvider.verify_token("fake.token")
            assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_fetch_keys_http_error_raises_503(self):
        from app.services.social_auth.apple_provider import AppleProvider
        with patch("app.services.social_auth.apple_provider.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.side_effect = Exception("network error")
            with pytest.raises(HTTPException) as exc_info:
                await AppleProvider._fetch_apple_public_keys()
            assert exc_info.value.status_code == 503


class TestGoogleProviderUnit:
    @pytest.mark.asyncio
    async def test_wrong_audience_raises_401(self):
        from app.services.social_auth.google_provider import GoogleProvider
        mock_payload = {"aud": "other-app-client-id", "email": "u@g.com", "email_verified": True}
        with patch.object(GoogleProvider, "_call_tokeninfo", new_callable=AsyncMock, return_value=mock_payload):
            with pytest.raises(HTTPException) as exc_info:
                await GoogleProvider.verify_token("fake.google.token")
            assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_unverified_email_raises_401(self):
        from app.services.social_auth.google_provider import GoogleProvider
        from app.core.config import settings
        mock_payload = {
            "aud": settings.GOOGLE_CLIENT_ID,
            "email": "unverified@g.com",
            "email_verified": False,
        }
        with patch.object(GoogleProvider, "_call_tokeninfo", new_callable=AsyncMock, return_value=mock_payload):
            with pytest.raises(HTTPException) as exc_info:
                await GoogleProvider.verify_token("fake.google.token")
            assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_tokeninfo_non_200_raises_401(self):
        from app.services.social_auth.google_provider import GoogleProvider
        mock_response = MagicMock()
        mock_response.status_code = 400
        with patch("app.services.social_auth.google_provider.httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.get = AsyncMock(return_value=mock_response)
            with pytest.raises(HTTPException) as exc_info:
                await GoogleProvider._call_tokeninfo("bad.token")
            assert exc_info.value.status_code == 401


class TestFacebookProviderUnit:
    @pytest.mark.asyncio
    async def test_invalid_token_raises_401(self):
        from app.services.social_auth.facebook_provider import FacebookProvider
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"is_valid": False, "app_id": "123"}}
        with patch("app.services.social_auth.facebook_provider.httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.get = AsyncMock(return_value=mock_response)
            with pytest.raises(HTTPException) as exc_info:
                await FacebookProvider._debug_token("bad.token")
            assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_wrong_app_id_raises_401(self):
        from app.services.social_auth.facebook_provider import FacebookProvider
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"is_valid": True, "app_id": "wrong_app_id"}}
        with patch("app.services.social_auth.facebook_provider.httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.get = AsyncMock(return_value=mock_response)
            with pytest.raises(HTTPException) as exc_info:
                await FacebookProvider._debug_token("token")
            assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_missing_email_in_profile_raises_401(self):
        from app.services.social_auth.facebook_provider import FacebookProvider
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "fb123", "name": "No Email"}
        with patch("app.services.social_auth.facebook_provider.httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_instance
            mock_instance.get = AsyncMock(return_value=mock_response)
            with pytest.raises(HTTPException) as exc_info:
                await FacebookProvider._fetch_user_info("token")
            assert exc_info.value.status_code == 401
