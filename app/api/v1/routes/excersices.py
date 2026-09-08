from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.controllers.excersices.condition_controller import condition_controller
from app.controllers.excersices.equipment_controller import equipment_controller
from app.controllers.excersices.everyday_item_controller import everyday_item_controller
from app.controllers.excersices.excersice_controller import excersice_controller
from app.controllers.excersices.goal_controller import goal_controller
from app.controllers.excersices.gym_equipment_controller import gym_equipment_controller
from app.controllers.excersices.health_question_controller import (
    health_question_controller,
)
from app.controllers.excersices.home_equipment_controller import (
    home_equipment_controller,
)
from app.controllers.excersices.leisure_activity_controller import (
    leisure_activity_controller,
)
from app.controllers.excersices.level_controller import level_controller
from app.controllers.excersices.method_controller import method_controller
from app.controllers.excersices.outdoor_equipment_controller import (
    outdoor_equipment_controller,
)
from app.controllers.excersices.session_duration_controller import (
    session_duration_controller,
)
from app.controllers.excersices.workout_hybrid_places_controller import (
    workou_hybrid_places_controller,
)
from app.controllers.excersices.workout_place_controller import workout_place_controller
from app.models import BodyPart, Equipment, ExerciseType, Muscle
from app.schemas.exercises import (
    BodyPartResponse,
    EquipmentCatalogResponse,
    ExerciseTypeResponse,
    MuscleResponse,
)
from app.schemas.training import (
    ConditionSchema,
    EquipmentCategoriesResponse,
    EquipmentSchema,
    EveryDayItemSchema,
    ExcersiceResponse,
    GoalSchema,
    GymEquipmentSchema,
    HomeEquipmentSchema,
    LevelSchema,
    MethodSchema,
    OutdoorEquipmentSchema,
    SessionDurationSchema,
    WorkOutHybridPalcesSchema,
    WorkoutPlacementSchema,
)
from app.schemas.training.health_question_schema import HealthQuestionSchema
from app.schemas.training.leisure_activity_schema import LeisureActivitySchema

router = APIRouter()


@router.get(
    "/levels", response_model=list[LevelSchema], summary="Listar niveles de experiencia"
)
def get_levels(db: Session = Depends(deps.get_db)) -> list[LevelSchema]:
    return level_controller.list_levels(db)


@router.get(
    "/goals", response_model=list[GoalSchema], summary="Listar objetivos de la app"
)
def get_goals(db: Session = Depends(deps.get_db)) -> list[GoalSchema]:

    return goal_controller.list_goals(db)


@router.get(
    "/conditions",
    response_model=list[ConditionSchema],
    summary="Listar condiciones médicas (patologías y enfermedades)",
)
def get_conditions(
    type: str | None = Query(
        None, description="Filtrar por tipo: 'PATHOLOGY' o 'DISEASE'"
    ),
    db: Session = Depends(deps.get_db),
) -> list[ConditionSchema]:

    return condition_controller.list_conditions(db, type=type)


@router.get(
    "/methods",
    response_model=list[MethodSchema],
    summary="Listar métodos de entrenamiento",
)
def get_methods(
    category: str | None = Query(
        None, description="Filtrar por categoría: 'FORCE' o 'RESISTANCE'"
    ),
    db: Session = Depends(deps.get_db),
) -> list[MethodSchema]:

    return method_controller.list_methods(db, category=category)


@router.get(
    "",
    response_model=list[ExcersiceResponse],
    summary="Listar y buscar ejercicios por nombre, grupo muscular o patología",
)
def get_excersices(
    name: str | None = Query(
        None, description="Buscar por nombre o término (ej: 'Bench Press', 'Push-up')"
    ),
    muscle_group: str | None = Query(
        None, description="Filtrar por grupo muscular (ej: 'Pecho', 'Pierna')"
    ),
    pattern: str | None = Query(None, description="Filtrar por patrón de movimiento"),
    level: str | None = Query(
        None, description="Filtrar por nivel sugerido (ej: 'Intermedio')"
    ),
    goal_code: str | None = Query(
        None, description="Filtrar por código de objetivo (ej: 'PG')"
    ),
    exclude_conditions: list[str] | None = Query(
        None,
        alias="exclude_conditions",
        description="Códigos de condiciones médicas a excluir (ej: ['PAT002'])",
    ),
    db: Session = Depends(deps.get_db),
) -> list[ExcersiceResponse]:

    return excersice_controller.list_excersices(
        db,
        name=name,
        muscle_group=muscle_group,
        pattern=pattern,
        level=level,
        goal_code=goal_code,
        exclude_condition_codes=exclude_conditions,
    )


@router.get(
    "/equipments",
    response_model=list[EquipmentSchema],
    summary="Listar equipamiento de entrenamiento",
)
def get_equipments(db: Session = Depends(deps.get_db)) -> list[EquipmentSchema]:

    return equipment_controller.list_equipments(db)


@router.get(
    "/session_durations",
    response_model=list[SessionDurationSchema],
    summary="Listar duraciones de sesión disponibles",
)
def get_session_durations(
    db: Session = Depends(deps.get_db),
) -> list[SessionDurationSchema]:

    return session_duration_controller.list_session_duration(db)


@router.get(
    "/workout-places",
    response_model=list[WorkoutPlacementSchema],
    summary="Listar lugares de entrenamiento disponibles",
)
def list_workout_places(
    db: Session = Depends(deps.get_db),
) -> list[WorkoutPlacementSchema]:

    return workout_place_controller.list_workout_place(db)


@router.get(
    "/hybrid-places",
    response_model=list[WorkOutHybridPalcesSchema],
    summary="Listar lugares Hybridos de entrenamiento",
)
def list_hybrid_workout_places(
    db: Session = Depends(deps.get_db),
) -> list[WorkOutHybridPalcesSchema]:
    return workou_hybrid_places_controller.list_workout_hybrid_places(db=db)


@router.get(
    "/everyday_tiems",
    response_model=list[EveryDayItemSchema],
    summary="Listar elementos de uso diario",
)
def list_everyday_items(db: Session = Depends(deps.get_db)) -> list[EveryDayItemSchema]:
    return everyday_item_controller.list_everyday_item_controller(db=db)


@router.get(
    "/equipments/categories",
    response_model=EquipmentCategoriesResponse,
    summary="Listar categorías de equipamiento",
)
def get_equipment_categories(
    db: Session = Depends(deps.get_db),
) -> EquipmentCategoriesResponse:
    return equipment_controller.get_equipment_categories(db)


@router.get(
    "/gym-equipments",
    response_model=list[GymEquipmentSchema],
    summary="Listar equipamiento de gimnasio disponible",
)
def get_gym_equipments(db: Session = Depends(deps.get_db)) -> list[GymEquipmentSchema]:
    return gym_equipment_controller.list_gym_equipment(db)


@router.get(
    "/home-equipments",
    response_model=list[HomeEquipmentSchema],
    summary="Listar equipamiento de casa disponible",
)
def get_home_equipments(
    db: Session = Depends(deps.get_db),
) -> list[HomeEquipmentSchema]:
    return home_equipment_controller.list_home_equipment(db)


@router.get(
    "/outdoor-equipments",
    response_model=list[OutdoorEquipmentSchema],
    summary="Listar equipamiento de exterior disponible",
)
def get_outdoor_equipments(
    db: Session = Depends(deps.get_db),
) -> list[OutdoorEquipmentSchema]:
    return outdoor_equipment_controller.list_outdoor_equipment(db)


@router.get(
    "/everyday-items",
    response_model=list[EveryDayItemSchema],
    summary="Listar elementos de uso diario (formato alternativo)",
)
def get_everyday_items(db: Session = Depends(deps.get_db)) -> list[EveryDayItemSchema]:
    return everyday_item_controller.list_everyday_item_controller(db=db)


@router.get(
    "/leisure-activities",
    response_model=list[LeisureActivitySchema],
    summary="Listar actividades de tiempo libre",
)
def get_leisure_activities(
    db: Session = Depends(deps.get_db),
) -> list[LeisureActivitySchema]:
    return leisure_activity_controller.list_leisure_activities(db)


@router.get(
    "/health-questions",
    response_model=list[HealthQuestionSchema],
    summary="Listar preguntas de salud",
)
def get_health_questions(
    db: Session = Depends(deps.get_db),
) -> list[HealthQuestionSchema]:
    return health_question_controller.list_health_questions(db)


# MARK: - Anatomical & ExerciseDB Catalogs


@router.get(
    "/body-parts",
    response_model=list[BodyPartResponse],
    summary="Listar partes del cuerpo con imágenes CDN (Español / Inglés)",
)
def get_body_parts(db: Session = Depends(deps.get_db)) -> list[BodyPartResponse]:
    return db.query(BodyPart).order_by(BodyPart.id).all()


@router.get(
    "/exercise-types",
    response_model=list[ExerciseTypeResponse],
    summary="Listar tipos/disciplinas de ejercicio con imágenes CDN (Español / Inglés)",
)
def get_exercise_types(
    db: Session = Depends(deps.get_db),
) -> list[ExerciseTypeResponse]:
    return db.query(ExerciseType).order_by(ExerciseType.id).all()


@router.get(
    "/muscles",
    response_model=list[MuscleResponse],
    summary="Listar músculos anatómicos (Latín / Español)",
)
def get_muscles(db: Session = Depends(deps.get_db)) -> list[MuscleResponse]:
    return db.query(Muscle).order_by(Muscle.id).all()


@router.get(
    "/equipments/catalog",
    response_model=list[EquipmentCatalogResponse],
    summary="Listar catálogo completo de equipamiento con imágenes CDN (Español / Inglés)",
)
def get_equipments_catalog(
    db: Session = Depends(deps.get_db),
) -> list[EquipmentCatalogResponse]:
    return (
        db.query(Equipment)
        .filter(Equipment.image_url.isnot(None))
        .order_by(Equipment.id)
        .all()
    )
