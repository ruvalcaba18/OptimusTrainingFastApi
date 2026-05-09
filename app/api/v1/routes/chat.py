from fastapi import APIRouter, Depends
from typing import Any
from sqlalchemy.orm import Session

from app.database import get_db
from app.api import deps
from app.controllers.chat.chat_controller import chat_controller
from app.schemas.chat.chat import ChatRequest
from app.models.user import User

router = APIRouter()

@router.post("/completions")
async def chat_with_openai(
    chat_request: ChatRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    
    return await chat_controller.chat_with_openai(chat_request, current_user, db)