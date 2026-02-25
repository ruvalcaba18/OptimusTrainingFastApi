"""
Response genérica para mensajes simples (ej. "eliminado", "enviado").
Úsala cuando el endpoint no necesita devolver un objeto complejo.

Ejemplo:
    return MessageResponse(message="Foto eliminada correctamente")
"""
from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str
    success: bool = True
