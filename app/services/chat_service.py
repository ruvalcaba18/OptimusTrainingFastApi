import httpx
from typing import Any, Dict
from app.core.config import settings
from app.core.redis_client import get_redis
from app.schemas.chat import ChatRequest

class ChatService:
    CHAT_COUNTER_KEY = "global_chat_calls_lifetime_count"
    CHAT_MAX_TOTAL = 100

    async def get_global_count(self) -> int:
        redis = await get_redis()
        try:
            count = await redis.get(self.CHAT_COUNTER_KEY)
            return int(count) if count else 0
        except (ValueError, TypeError):
            return 0

    async def increment_global_count(self) -> int:
        redis = await get_redis()
        return await redis.incr(self.CHAT_COUNTER_KEY)

    async def call_openai_proxy(self, chat_in: ChatRequest) -> Dict[str, Any]:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API Key no configurada en el servidor.")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": chat_in.model,
                    "messages": [m.model_dump() for m in chat_in.messages],
                    "temperature": chat_in.temperature
                },
                timeout=45.0
            )
            
            if response.status_code != 200:
                raise Exception(f"OpenAI Error: {response.text}")
                
            return response.json()

chat_service = ChatService()
