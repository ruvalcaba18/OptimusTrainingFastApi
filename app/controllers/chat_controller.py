from datetime import timedelta
from fastapi import HTTPException, status
from typing import Any, Dict
from app.services.chat_service import chat_service
from app.schemas.chat import ChatRequest
from app.models.user import User
from app.core import security
from app.core.config import settings

class ChatController:
    @staticmethod
    async def chat_with_openai(chat_in: ChatRequest, current_user: User) -> Dict[str, Any]:
        current_count = await chat_service.get_global_count()
        if current_count >= chat_service.CHAT_MAX_TOTAL:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Límite de prueba alcanzado ({chat_service.CHAT_MAX_TOTAL}/{chat_service.CHAT_MAX_TOTAL})."
            )

        try:
            result = await chat_service.call_openai_proxy(chat_in)
            await chat_service.increment_global_count()
            return result
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en el proxy de Chat: {str(e)}")

chat_controller = ChatController()
