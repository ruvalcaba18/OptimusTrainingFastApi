from pathlib import Path

from sqlalchemy.orm import Session

from app.database.seeders.base_seeder import BaseSeeder
from app.models import (
    EverydayItem,
    GymEquipmentModel,
    HealthQuestionModel,
    HomeEquipmentModel,
    LeisureActivityModel,
    Method,
    OutdoorEquipmentModel,
    ProgrammingMatrix,
    SessionDuration,
    WorkoutHybridPlaces,
    WorkoutPlace,
)
from app.models.Enums.EverydayItems import EverydayItems
from app.models.Enums.GymEquipment import GymEquipment
from app.models.Enums.HomeEquipment import HomeEquipment
from app.models.Enums.OutdoorEquipment import OutdoorEquipment


class AssessmentSeeder(BaseSeeder):
    def seed(self) -> None:
        self.seed_session_durations()
        self.seed_workout_places()
        self.seed_workout_hybrid_places()
        self.seed_everyday_items()
        self.seed_gym_equipment()
        self.seed_home_equipment()
        self.seed_outdoor_equipment()
        self.seed_leisure_activities()
        self.seed_health_questions()

    def seed_session_durations(self):
        print("Seeding session durations...")
        data = [
            ("EXPRESS",  "Express (15-30 min)",   "Sesiones rápidas y de alta intensidad."),
            ("STANDARD", "Estándar (45-60 min)",   "El tiempo ideal para un entrenamiento completo."),
            ("EXTENDED", "Extendido (90+ min)",     "Para quienes disfrutan de sesiones largas y detalladas."),
            ("VARIABLE", "Variable",               "Mi tiempo cambia cada día y necesito flexibilidad."),
        ]
        for code, name, description in data:
            self.session.add(SessionDuration(code=code, name=name, description=description))
        self.session.commit()

    def seed_workout_places(self):
        print("Seeding workout places...")
        data = [
            ("gimnasio", "Gimnasio completo", "Tengo acceso a máquinas, pesas y racks."),
            ("casa",     "En casa",           "Entrenaré en mi hogar, con o sin equipo."),
            ("afuera",   "Al aire libre",     "Prefiero parques, pistas o barras al aire libre."),
            ("mixto",    "Híbrido",           "Combinaré diferentes lugares (casa, gym o parque)."),
        ]
        for code, name, description in data:
            self.session.add(WorkoutPlace(code=code, name=name, description=description))
        self.session.commit()

    def seed_workout_hybrid_places(self):
        data = [
            ("GYM", "Gimnasio" , "Haz pagado el gimnasio o deseas ir a un gimnasio"),
            ("HOUSE", "Casa", "Deseas hacer ejercicio en casa"),
            ("FREE", "Aire Libre", "Deseas hacer ejercicio al aire libre o mixto")
        ]
        for code, name, description in data:
            self.session.add(WorkoutHybridPlaces(code=code, name=name, description=description))
        self.session.commit()

    def seed_everyday_items(self):
        print("Seeding everyday items...")
        mappings = {
            EverydayItems.CHAIR: ("chair", "Silla de comedor o cualquier tipo de silla que se tenga en casa", "Silla,Banco"),
            EverydayItems.WATER_JUGS: ("waterJugs", "Cualquier tipo de garrafón es bueno incluso si no se tiene uno de 5 o 20 litros", "Garrafón,Peso"),
            EverydayItems.LOADED_BACKPACK: ("loadedBackpack", "Puedes cargarla de cualquier tipo de cosa en caso de no tener libros o arroz.", "Mochila,Peso"),
            EverydayItems.TOWELS: ("towels", "Cualquier tipo de toalla de cualquier tamaño", "Toalla"),
            EverydayItems.BROOMSTICK: ("broomstick", "O cualquier tipo de palo que te ayude a hacer ejercicio.", "Palo"),
            EverydayItems.STAIRS: ("stairs", " o cualquier parte que esté un poco elevada que te ayude a subir y bajar.", "Escalón"),
            EverydayItems.SOFA: ("sofa", "Sofá o Sillón", "Sofá"),
            EverydayItems.DETERGENT_BOTTLES: ("detergentBottles", "o botellas de agua", "Detergente,Peso"),
            EverydayItems.THICK_BOOKS: ("thickBooks", "o cualquier tipo de libro", "Libros,Peso"),
            EverydayItems.CLEAR_WALL: ("clearWall", "Pared Despejada", "Pared")
        }
        for enum_val, (code, description, mapping) in mappings.items():
            self.session.add(EverydayItem(code=code, name=enum_val.value, description=description, mapping=mapping))
        self.session.commit()

    def seed_gym_equipment(self):
        print("Seeding gym equipment...")
        mappings = {
            GymEquipment.DUMBBELLS: ("dumbbells", "Mancuernas,Mancuerna"),
            GymEquipment.MACHINES: ("machines", "Máquina"),
            GymEquipment.CABLES: ("cables", "Polea"),
            GymEquipment.RACKS: ("racks", "Smith,Máquina Smith"),
            GymEquipment.BARBELL: ("barbell", "Barra"),
            GymEquipment.PLYO_BOX: ("plyoBox", "Cajón Pliométrico"),
            GymEquipment.HEAVY_BAG: ("heavyBag", "Costal"),
            GymEquipment.ASSAULT_BIKE: ("assaultBike", "Bicicleta"),
            GymEquipment.BENCHES: ("benches", "Banco"),
            GymEquipment.KETTLEBELLS: ("kettlebells", "Kettlebell")
        }
        for enum_val, (code, mapping) in mappings.items():
            self.session.add(GymEquipmentModel(code=code, name=enum_val.value, mapping=mapping))
        self.session.commit()

    def seed_home_equipment(self):
        print("Seeding home equipment...")
        mappings = {
            HomeEquipment.RESISTANCE_BANDS: ("resistanceBands", "Banda"),
            HomeEquipment.MINI_BANDS: ("miniBands", "Banda"),
            HomeEquipment.ADJUSTABLE_DUMBBELLS: ("adjustableDumbbells", "Mancuernas,Mancuerna"),
            HomeEquipment.JUMP_ROPE: ("jumpRope", "Cuerda"),
            HomeEquipment.PULLUP_RACK: ("pullupRack", "Smith"),
            HomeEquipment.PULLUP_BAR: ("pullupBar", "Barra"),
            HomeEquipment.YOGA_MAT: ("yogaMat", "Colchoneta"),
            HomeEquipment.AB_WHEEL: ("abWheel", "Rueda"),
            HomeEquipment.ANKLE_WEIGHTS: ("ankleWeights", "Peso"),
            HomeEquipment.SWISS_BALL: ("swissBall", "Pelota")
        }
        for enum_val, (code, mapping) in mappings.items():
            self.session.add(HomeEquipmentModel(code=code, name=enum_val.value, mapping=mapping))
        self.session.commit()

    def seed_outdoor_equipment(self):
        print("Seeding outdoor equipment...")
        mappings = {
            OutdoorEquipment.TRACK: ("track", "Pista"),
            OutdoorEquipment.PULLUP_BARS: ("pullupBars", "Barra"),
            OutdoorEquipment.PARALLEL_BARS: ("parallelBars", "Paralelas"),
            OutdoorEquipment.CONCRETE_BENCHES: ("concreteBenches", "Banco"),
            OutdoorEquipment.MONKEY_BARS: ("monkeyBars", "Pasamanos"),
            OutdoorEquipment.HILLS: ("hills", "Cuesta"),
            OutdoorEquipment.BLEACHERS: ("bleachers", "Gradas"),
            OutdoorEquipment.RINGS: ("rings", "Anillas"),
            OutdoorEquipment.LOW_WALLS: ("lowWalls", "Pared"),
            OutdoorEquipment.SAND: ("sand", "Arena")
        }
        for enum_val, (code, mapping) in mappings.items():
            self.session.add(OutdoorEquipmentModel(code=code, name=enum_val.value, mapping=mapping))
        self.session.commit()

    def seed_leisure_activities(self):
        print("Seeding leisure activities...")
        activities = [
            ("walking", "Caminar"),
            ("jogging", "Trotar y/o Sprints"),
            ("cycling", "Bicicleta (regular / estacionaria / de aire)"),
            ("dancing", "Bailar"),
            ("hiking", "Senderismo / Hike"),
            ("jumpRope", "Saltar la cuerda"),
            ("skating", "Patinar (Patines / Patineta / Patín)"),
            ("swimming", "Nadar"),
            ("aerobics", "Aerobics (jumping / barre / steps)"),
            ("yogaPilates", "Yoga / Pilates"),
            ("racketSports", "Tenis / Padel / Squash"),
            ("martialArts", "Boxeo / Artes Marciales (Recreativo)"),
            ("surfing", "Surf / Bodyboard"),
            ("climbing", "Escalada / Bouldering"),
            ("teamSports", "Deportes de equipo (Fútbol / Básquet / Voley)")
        ]
        for code, name in activities:
            self.session.add(LeisureActivityModel(code=code, name=name))
        self.session.commit()

    def seed_health_questions(self):
        print("Seeding health questions...")
        questions = [
            HealthQuestionModel(
                code="musculoskeletal",
                title="¿Presentas alguna lesión o condición musculoesquelética?",
                subtitle="Selecciona todas las que apliquen",
                type="multiple",
                category="PATHOLOGY"
            ),
            HealthQuestionModel(
                code="healthConditions",
                title="¿Presentas alguna condición de salud?",
                subtitle="Selecciona todas las que apliquen",
                type="multiple",
                category="DISEASE"
            )
        ]
        for q in questions:
            self.session.add(q)
        self.session.commit()

    def seed_programming_matrix(self):
        print("Seeding programming matrix...")
        methods_by_code = {m.code: m for m in self.session.query(Method).all()}
        rules = [
            {"goal": "PG", "level": "NIV1", "volume": "Bajo-Medio", "sets": 3, "reps": "12-15 reps", "rest": "30-45s", "method_code": "FMT008"},
            {"goal": "PG", "level": "NIV2", "volume": "Medio", "sets": 4, "reps": "12-15 reps", "rest": "30s", "method_code": "FMT004"},
            {"goal": "PG", "level": "NIV3", "volume": "Alto", "sets": 4, "reps": "10-12 reps", "rest": "30s", "method_code": "FMT005"},
            {"goal": "PG", "level": "NIV4", "volume": "Muy Alto", "sets": 5, "reps": "10-12 reps", "rest": "30s", "method_code": "FMT005"},
            {"goal": "GMM", "level": "NIV1", "volume": "Bajo", "sets": 3, "reps": "10-12 reps", "rest": "60-90s", "method_code": "FMT001"},
            {"goal": "GMM", "level": "NIV2", "volume": "Medio", "sets": 3, "reps": "8-12 reps", "rest": "60-90s", "method_code": "FMT002"},
            {"goal": "GMM", "level": "NIV3", "volume": "Alto", "sets": 4, "reps": "8-12 reps", "rest": "60-90s", "method_code": "FMT006"},
            {"goal": "GMM", "level": "NIV4", "volume": "Muy Alto", "sets": 4, "reps": "6-10 reps", "rest": "90s", "method_code": "FMT007"},
            {"goal": "SB", "level": "NIV1", "volume": "Bajo", "sets": 2, "reps": "12-15 reps", "rest": "60s", "method_code": "FMT001"},
            {"goal": "SB", "level": "NIV2", "volume": "Bajo-Medio", "sets": 3, "reps": "12-15 reps", "rest": "60s", "method_code": "FMT001"},
            {"goal": "SB", "level": "NIV3", "volume": "Medio", "sets": 3, "reps": "10-12 reps", "rest": "45-60s", "method_code": "FMT008"},
            {"goal": "SB", "level": "NIV4", "volume": "Medio", "sets": 3, "reps": "10-12 reps", "rest": "45s", "method_code": "FMT008"},
            {"goal": "RD", "level": "NIV1", "volume": "Bajo", "sets": 3, "reps": "8-10 reps", "rest": "90-120s", "method_code": "FMT001"},
            {"goal": "RD", "level": "NIV2", "volume": "Medio", "sets": 3, "reps": "6-8 reps", "rest": "120s", "method_code": "FMT003"},
            {"goal": "RD", "level": "NIV3", "volume": "Alto", "sets": 4, "reps": "4-6 reps", "rest": "150-180s", "method_code": "FMT009"},
            {"goal": "RD", "level": "NIV4", "volume": "Muy Alto", "sets": 5, "reps": "1-5 reps", "rest": "180s", "method_code": "FMT009"},
        ]
        for r in rules:
            method = methods_by_code.get(r["method_code"])
            pm = ProgrammingMatrix(
                goal_code=r["goal"], level_code=r["level"], volume=r["volume"],
                sets=r["sets"], reps=r["reps"], rest=r["rest"], method_id=method.id if method else None
            )
            self.session.add(pm)
        self.session.commit()
