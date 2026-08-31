from pathlib import Path
from typing import final

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.database.seeders import (
    AnatomySeeder,
    AssessmentSeeder,
    CatalogsSeeder,
    EquipmentSeeder,
    ExercisesSeeder,
)
from app.models import (
    BodyPart,
    Condition,
    Equipment,
    EverydayItem,
    Excersice,
    ExcersiceCondition,
    ExcersiceEquipment,
    ExcersiceGoal,
    ExcersiceMuscle,
    ExerciseType,
    Goal,
    GymEquipmentModel,
    HealthQuestionModel,
    HomeEquipmentModel,
    LeisureActivityModel,
    Level,
    Method,
    MethodGoal,
    Muscle,
    OutdoorEquipmentModel,
    ProgrammingMatrix,
    SessionDuration,
    WorkoutHybridPlaces,
    WorkoutPlace,
)


@final
class DatabaseSeeder:
    def __init__(self, session: Session, data_dir: Path):
        self.session = session
        self.data_dir = data_dir

    def seed_all(self, include_matrix: bool = True):
        self.clear_database()

        # 1. Catálogos base (Niveles, Objetivos, Condiciones, Métodos)
        catalogs = CatalogsSeeder(self.session, self.data_dir)
        catalogs.seed()

        # 2. Anatomía (Partes del cuerpo, Tipos de ejercicio, Músculos)
        anatomy = AnatomySeeder(self.session, self.data_dir)
        anatomy.seed()

        # 3. Equipamiento (Catálogo bilingüe y CDN)
        equipment = EquipmentSeeder(self.session, self.data_dir)
        equipment.seed()

        # 4. Ejercicios y sus relaciones con anatomía, equipos y patologías
        exercises = ExercisesSeeder(
            self.session,
            self.data_dir,
            goals_map=catalogs.goals_map,
            conditions_map=catalogs.conditions_map,
            equip_map=equipment.equip_map,
            muscles_map=anatomy.muscles_map
        )
        exercises.seed()

        # 5. Parámetros del Assessment y Matriz de Programación
        assessment = AssessmentSeeder(self.session, self.data_dir)
        assessment.seed()

        if include_matrix:
            assessment.seed_programming_matrix()

    def clear_database(self):
        print("Clearing database tables...")
        self.session.query(ExcersiceMuscle).delete()
        self.session.query(Muscle).delete()
        self.session.query(BodyPart).delete()
        self.session.query(ExerciseType).delete()
        self.session.query(ExcersiceCondition).delete()
        self.session.query(ExcersiceEquipment).delete()
        self.session.query(ExcersiceGoal).delete()
        self.session.query(MethodGoal).delete()
        self.session.query(Excersice).delete()
        self.session.query(Method).delete()
        self.session.query(Condition).delete()
        self.session.query(Goal).delete()
        self.session.query(Level).delete()
        self.session.query(Equipment).delete()
        self.session.query(ProgrammingMatrix).delete()
        self.session.query(SessionDuration).delete()
        self.session.query(WorkoutPlace).delete()
        self.session.query(WorkoutHybridPlaces).delete()
        self.session.query(EverydayItem).delete()
        self.session.query(GymEquipmentModel).delete()
        self.session.query(HomeEquipmentModel).delete()
        self.session.query(OutdoorEquipmentModel).delete()
        self.session.query(LeisureActivityModel).delete()
        self.session.query(HealthQuestionModel).delete()
        self.session.commit()

def seed_database():
    data_dir = Path(__file__).parent / "data"
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found at: {data_dir}")
        
    session = SessionLocal()
    try:
        seeder = DatabaseSeeder(session, data_dir)
        seeder.seed_all()
        print("🎉 All seeds executed successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error during seeding: {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
