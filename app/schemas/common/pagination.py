"""
Paginación genérica.
Úsala en cualquier endpoint que devuelva listas.

Ejemplo:
    @router.get("/", response_model=PaginatedResponse[UserResponse])
    def list_users(...):
        items = user_service.get_multi(db, skip=skip, limit=limit)
        total = user_service.count(db)
        return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)
"""
from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    skip: int
    limit: int
    has_more: bool = False

    @classmethod
    def from_items(cls, items: List[T], total: int, skip: int, limit: int) -> "PaginatedResponse[T]":
        return cls(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
            has_more=(skip + limit) < total,
        )
