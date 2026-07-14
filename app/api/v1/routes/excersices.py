from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.controllers.excersices.level_controller import level_controller
from app.controllers.excersices.goal_controller import goal_controller
from app.controllers.excersices.condition_controller import condition_controller
from app.controllers.excersices.method_controller import method_controller
from app.controllers.excersices.excersice_controller import excersice_controller
from app.controllers.excersices.equipment_controller import equipment_controller
from app.schemas.training import (
    LevelSchema,
    GoalSchema,
    ConditionSchema,
    MethodSchema,
    ExcersiceResponse,
    EquipmentSchema,
)

router = APIRouter()

@router.get("/levels", response_model=List[LevelSchema], summary="Listar niveles de experiencia")
def get_levels(db: Session = Depends(deps.get_db)):
    """
    Retorna la lista de niveles de experiencia del usuario definidos en la aplicación.
    """
    return level_controller.list_levels(db)

@router.get("/goals", response_model=List[GoalSchema], summary="Listar objetivos de la app")
def get_goals(db: Session = Depends(deps.get_db)):
    """
    Retorna la lista de objetivos (Pérdida de Grasa, Ganancia de Masa Muscular, etc.).
    """
    return goal_controller.list_goals(db)

@router.get("/conditions", response_model=List[ConditionSchema], summary="Listar condiciones médicas (patologías y enfermedades)")
def get_conditions(
    type: Optional[str] = Query(None, description="Filtrar por tipo: 'PATHOLOGY' o 'DISEASE'"),
    db: Session = Depends(deps.get_db)
):
    """
    Retorna el catálogo de patologías y enfermedades del usuario.
    """
    return condition_controller.list_conditions(db, type=type)

@router.get("/methods", response_model=List[MethodSchema], summary="Listar métodos de entrenamiento")
def get_methods(
    category: Optional[str] = Query(None, description="Filtrar por categoría: 'FORCE' o 'RESISTANCE'"),
    db: Session = Depends(deps.get_db)
):
    """
    Retorna los métodos de entrenamiento con sus objetivos prioritarios cargados.
    """
    return method_controller.list_methods(db, category=category)

@router.get("/", response_model=List[ExcersiceResponse], summary="Listar y filtrar ejercicios (motor de decisión)")
def get_excersices(
    muscle_group: Optional[str] = Query(None, description="Filtrar por grupo muscular (ej: 'Pierna')"),
    pattern: Optional[str] = Query(None, description="Filtrar por patrón de movimiento"),
    level: Optional[str] = Query(None, description="Filtrar por nivel sugerido (ej: 'Intermedio')"),
    goal_code: Optional[str] = Query(None, description="Filtrar por código de objetivo (ej: 'PG')"),
    exclude_conditions: Optional[List[str]] = Query(None, alias="exclude_conditions", description="Códigos de condiciones médicas a excluir (ej: ['PAT002'])"),
    db: Session = Depends(deps.get_db)
):
    """
    Listado principal de ejercicios. Soporta filtros dinámicos y la exclusión de ejercicios
    clasificados como 'FORBIDDEN' para las condiciones indicadas en 'exclude_conditions'.
    """
    return excersice_controller.list_excersices(
        db,
        muscle_group=muscle_group,
        pattern=pattern,
        level=level,
        goal_code=goal_code,
        exclude_condition_codes=exclude_conditions
    )

@router.get("/equipments", response_model=List[EquipmentSchema], summary="Listar equipamiento de entrenamiento")
def get_equipments(db: Session = Depends(deps.get_db)):
    """
    Retorna la lista de equipamientos cargados en la aplicación.
    """
    return equipment_controller.list_equipments(db)

