from datetime import timedelta
from fastapi import HTTPException, status
from typing import Any, Dict
from sqlalchemy.orm import Session 

from app.services.chat_service import chat_service
from app.schemas.chat.chat import ChatRequest
from app.models.user import User
from app.core import security
from app.core.config import settings
from app.models.prompt_log import PromptLog

class ChatController:
    @staticmethod
    async def chat_with_openai(chat_in: ChatRequest, current_user: User, db: Session) -> Dict[str, Any]:
        current_count = await chat_service.get_global_count()
        
        if current_count >= chat_service.CHAT_MAX_TOTAL:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Límite de prueba alcanzado ({chat_service.CHAT_MAX_TOTAL}/{chat_service.CHAT_MAX_TOTAL})."
            )

        try:
            result = await chat_service.call_openai_proxy(chat_in)
            await chat_service.increment_global_count()
            
            new_log = ChatController.build_prompt_log(
                chat_in=chat_in,
                current_user=current_user,
                result=result
            )
            
            ChatController.save_prompt_log(
                db = db, 
                new_log = new_log
            )
            
            
            return result
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en el proxy de Chat: {str(e)}")
        
    
    @staticmethod
    def build_prompt_log(
        chat_in: ChatRequest,
        current_user: User,
        result: Dict[str, Any]
    ) -> PromptLog:
        system_prompt = next(
            (msg.content for msg in chat_in.messages if msg.role == "system"),
            ""
        )
        user_prompt = next(
            (msg.content for msg in chat_in.messages if msg.role == "user"),
            ""
        )
        
        ai_response = (
            result.get("choices", [{}])[0]
            .get("message",{})
            .get("content", "")
        )
        
        return PromptLog(
            user_id = current_user.id,
            system_prompt = system_prompt,
            user_prompt = user_prompt,
            ai_response = ai_response
        )
    
    @staticmethod
    def save_prompt_log(db: Session, prompt_log: PromptLog) -> None:
        db.add(prompt_log)
        db.commit()

chat_controller = ChatController()
