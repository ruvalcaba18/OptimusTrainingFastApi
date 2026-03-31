import httpx
from fastapi import HTTPException, status
from app.core.config import settings


FACEBOOK_GRAPH_URL = "https://graph.facebook.com"


class FacebookProvider:

    @staticmethod
    async def verify_token(token: str) -> dict:
        await FacebookProvider._debug_token(token)
        return await FacebookProvider._fetch_user_info(token)

    # ── Private

    @staticmethod
    async def _debug_token(token: str) -> None:
        app_access_token = f"{settings.FACEBOOK_APP_ID}|{settings.FACEBOOK_APP_SECRET}"

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    f"{FACEBOOK_GRAPH_URL}/debug_token",
                    params={
                        "input_token": token,
                        "access_token": app_access_token,
                    },
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No se pudo contactar a Facebook para verificar el token",
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Facebook token inválido",
            )

        data: dict = response.json().get("data", {})

        if not data.get("is_valid", False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Facebook token inválido o expirado",
            )

        if str(data.get("app_id")) != str(settings.FACEBOOK_APP_ID):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Facebook token inválido — App ID no coincide",
            )

    @staticmethod
    async def _fetch_user_info(token: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    f"{FACEBOOK_GRAPH_URL}/me",
                    params={
                        "fields": "id,name,email",
                        "access_token": token,
                    },
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No se pudo obtener el perfil de Facebook",
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Facebook token inválido — no se pudo obtener el perfil",
            )

        data = response.json()
        email = data.get("email")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=(
                    "No se pudo obtener el email desde Facebook. "
                    "Asegúrate de solicitar el permiso 'email' en el cliente."
                ),
            )

        return {
            "email": email.lower().strip(),
            "name": data.get("name"),
            "provider_id": data.get("id"),
        }
