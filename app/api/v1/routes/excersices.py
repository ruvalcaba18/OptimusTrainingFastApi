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
from app.controllers.excersices.session_duration_controller import session_duration_controller
from app.controllers.excersices.workout_place_controller import workout_place_controller

from app.schemas.training import (
    LevelSchema,
    GoalSchema,
    ConditionSchema,
    MethodSchema,
    ExcersiceResponse,
    EquipmentSchema,
    SessionDurationSchema, 
    WorkoutPlacementSchema
)

router = APIRouter()

@router.get("/levels", response_model=List[LevelSchema], summary="Listar niveles de experiencia")
def get_levels(db: Session = Depends(deps.get_db)) -> List[LevelSchema]:
    return level_controller.list_levels(db)

@router.get("/goals", response_model=List[GoalSchema], summary="Listar objetivos de la app")
def get_goals(db: Session = Depends(deps.get_db)) -> List[GoalSchema]:
    
    return goal_controller.list_goals(db)

@router.get("/conditions", response_model=List[ConditionSchema], summary="Listar condiciones médicas (patologías y enfermedades)")
def get_conditions(
    type: Optional[str] = Query(None, description="Filtrar por tipo: 'PATHOLOGY' o 'DISEASE'"),
    db: Session = Depends(deps.get_db)
) -> List[ConditionSchema]:
  
    return condition_controller.list_conditions(db, type=type)

@router.get("/methods", response_model=List[MethodSchema], summary="Listar métodos de entrenamiento")
def get_methods(
    category: Optional[str] = Query(None, description="Filtrar por categoría: 'FORCE' o 'RESISTANCE'"),
    db: Session = Depends(deps.get_db)
) -> List[MethodSchema]:
  
    return method_controller.list_methods(db, category=category)

@router.get(
"/", 
response_model=List[ExcersiceResponse],
summary="Listar y filtrar ejercicios (motor de decisión)"
)
def get_excersices(
    muscle_group: Optional[str] = Query(None, description="Filtrar por grupo muscular (ej: 'Pierna')"),
    pattern: Optional[str] = Query(None, description="Filtrar por patrón de movimiento"),
    level: Optional[str] = Query(None, description="Filtrar por nivel sugerido (ej: 'Intermedio')"),
    goal_code: Optional[str] = Query(None, description="Filtrar por código de objetivo (ej: 'PG')"),
    exclude_conditions: Optional[List[str]] = Query(None, alias="exclude_conditions", description="Códigos de condiciones médicas a excluir (ej: ['PAT002'])"),
    db: Session = Depends(deps.get_db)
) -> List[ExcersiceResponse]:
   
    return excersice_controller.list_excersices(
        db,
        muscle_group=muscle_group,
        pattern=pattern,
        level=level,
        goal_code=goal_code,
        exclude_condition_codes=exclude_conditions
    )

@router.get(
"/equipments", 
response_model=List[EquipmentSchema], 
summary="Listar equipamiento de entrenamiento"
)
def get_equipments(
    db: Session = Depends(deps.get_db)
) -> List[EquipmentSchema]:
    
    return equipment_controller.list_equipments(db)

@router.get("/session_durations",
            response_model=List[SessionDurationSchema],
            summary="Listar duraciones de sesión disponibles"
)
def get_session_durations(db: Session = Depends(deps.get_db)) -> List[SessionDurationSchema]:
    
    return session_duration_controller.list_session_duration(db)
 
@router.get("/workout-places",
             response_model=List[WorkoutPlacementSchema],
             summary="Listar lugares de entrenamiento disponibles")
def list_workout_places(db: Session = Depends(deps.get_db)) -> List[WorkoutPlacementSchema]:
     
     return workout_place_controller.list_workout_place(db)