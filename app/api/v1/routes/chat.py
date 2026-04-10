from fastapi import APIRouter, Depends
from typing import Any, Dict

from app.api import deps
from app.controllers.chat_controller import chat_controller
from app.schemas.chat import ChatRequest
from app.models.user import User

router = APIRouter()

@router.post("/completions")
async def chat_with_openai(
    chat_request: ChatRequest,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Proxy seguro para OpenAI siguiendo el patrón Route -> Controller -> Service.
    Límite global: 100 peticiones en total.
    """
    return await chat_controller.chat_with_openai(chat_request, current_user)