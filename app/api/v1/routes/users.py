"""
User routes for API v1.
Thin layer: validates HTTP input, calls controller, returns response.
"""
from typing import Any
from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.users.user_controller import user_controller
from app.schemas.users import UserCreate, UserResponse, UserUpdate
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=list[UserResponse], summary="Listar usuarios")
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna una lista paginada de usuarios. Requiere autenticación."""
    return user_controller.list_users(db, skip=skip, limit=limit)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Crear usuario")
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> Any:
    """Registra un nuevo usuario deportivo."""
    return user_controller.create_user(db, user_in=user_in)


@router.get("/me", response_model=UserResponse, summary="Mi perfil")
def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """Devuelve el perfil del usuario autenticado."""
    return current_user


@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID")
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return user_controller.get_user(db, user_id=user_id)


@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar usuario")
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return user_controller.update_user(db, user_id=user_id, user_in=user_in, current_user=current_user)


@router.post(
    "/{user_id}/photo",
    response_model=UserResponse,
    summary="Subir foto de perfil",
    description="Sube una foto JPG/PNG/WEBP de hasta 5 MB como foto de perfil.",
)
async def upload_profile_picture(
    user_id: int,
    file: UploadFile = File(..., description="Imagen de perfil (JPG, PNG o WEBP, máx 5 MB)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return await user_controller.upload_profile_picture(
        db, user_id=user_id, file=file, current_user=current_user
    )


@router.delete("/{user_id}", response_model=UserResponse, summary="Eliminar usuario")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    return user_controller.delete_user(db, user_id=user_id, current_user=current_user)
