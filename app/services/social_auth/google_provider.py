import httpx
from fastapi import HTTPException, status
from app.core.config import settings


GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"


class GoogleProvider:

    @staticmethod
    async def verify_token(token: str) -> dict:
        payload = await GoogleProvider._call_tokeninfo(token)

        aud = payload.get("aud")
        if aud != settings.GOOGLE_CLIENT_ID:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google token inválido — audience no coincide con GOOGLE_CLIENT_ID",
            )

        email = payload.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google token no contiene email",
            )

        if not payload.get("email_verified", False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El email de Google no está verificado",
            )

        return {
            "email": email.lower().strip(),
            "name": payload.get("name"),
            "provider_id": payload.get("sub"),
        }

    # ── Private

    @staticmethod
    async def _call_tokeninfo(token: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    GOOGLE_TOKEN_INFO_URL, params={"id_token": token}
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No se pudo contactar a Google para verificar el token",
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Google token inválido o expirado",
            )

        return response.json()
