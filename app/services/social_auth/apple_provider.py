import httpx
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.core.config import settings


APPLE_KEYS_URL = "https://appleid.apple.com/auth/keys"
APPLE_ISSUER = "https://appleid.apple.com"


class AppleProvider:

    @staticmethod
    async def verify_token(token: str) -> dict:
        keys = await AppleProvider._fetch_apple_public_keys()

        try:
            unverified_header = jwt.get_unverified_header(token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Apple token inválido — no se pudo leer el header",
            )

        matching_key = next(
            (k for k in keys if k.get("kid") == unverified_header.get("kid")),
            None,
        )
        if not matching_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Apple token inválido — clave pública no encontrada",
            )

        try:
            payload = jwt.decode(
                token,
                matching_key,
                algorithms=["RS256"],
                audience=settings.APPLE_CLIENT_ID,
                issuer=APPLE_ISSUER,
            )
        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Apple token inválido — {exc}",
            )

        email = payload.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Apple token no contiene email — asegúrate de solicitar el scope 'email'",
            )

        return {
            "email": email.lower().strip(),
            "name": None,
            "provider_id": payload.get("sub"),
        }

    # ── Private

    @staticmethod
    async def _fetch_apple_public_keys() -> list:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(APPLE_KEYS_URL)
                response.raise_for_status()
                return response.json().get("keys", [])
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No se pudo obtener las claves públicas de Apple",
            )
