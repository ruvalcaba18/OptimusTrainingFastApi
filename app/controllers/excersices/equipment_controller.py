from typing import List
from sqlalchemy.orm import Session
from app.services import equipment_service
from app.models import Equipment
from app.core.error_handlers import handle_controller_errors
from app.models.Enums.GymEquipment import GymEquipment
from app.models.Enums.HomeEquipment import HomeEquipment
from app.models.Enums.OutdoorEquipment import OutdoorEquipment
from app.models.Enums.EverydayItems import EverydayItems


class EquipmentController:

    @staticmethod
    @handle_controller_errors
    def list_equipments(db: Session) -> List[Equipment]:
        return equipment_service.list_equipments(db)

    @staticmethod
    @handle_controller_errors
    def get_equipment_categories() -> dict:
        return {
            "gym": [
                {"code": "dumbbells", "name": GymEquipment.DUMBBELLS.value, "mapping": ["Mancuernas", "Mancuerna"]},
                {"code": "machines", "name": GymEquipment.MACHINES.value, "mapping": ["Máquina"]},
                {"code": "cables", "name": GymEquipment.CABLES.value, "mapping": ["Polea"]},
                {"code": "racks", "name": GymEquipment.RACKS.value, "mapping": ["Smith", "Máquina Smith"]},
                {"code": "barbell", "name": GymEquipment.BARBELL.value, "mapping": ["Barra"]},
                {"code": "plyoBox", "name": GymEquipment.PLYO_BOX.value, "mapping": ["Cajón Pliométrico"]},
                {"code": "heavyBag", "name": GymEquipment.HEAVY_BAG.value, "mapping": ["Costal"]},
                {"code": "assaultBike", "name": GymEquipment.ASSAULT_BIKE.value, "mapping": ["Bicicleta"]},
                {"code": "benches", "name": GymEquipment.BENCHES.value, "mapping": ["Banco"]},
                {"code": "kettlebells", "name": GymEquipment.KETTLEBELLS.value, "mapping": ["Kettlebell"]}
            ],
            "home": [
                {"code": "resistanceBands", "name": HomeEquipment.RESISTANCE_BANDS.value, "mapping": ["Banda"]},
                {"code": "miniBands", "name": HomeEquipment.MINI_BANDS.value, "mapping": ["Banda"]},
                {"code": "adjustableDumbbells", "name": HomeEquipment.ADJUSTABLE_DUMBBELLS.value, "mapping": ["Mancuernas", "Mancuerna"]},
                {"code": "jumpRope", "name": HomeEquipment.JUMP_ROPE.value, "mapping": ["Cuerda"]},
                {"code": "pullupRack", "name": HomeEquipment.PULLUP_RACK.value, "mapping": ["Smith"]},
                {"code": "pullupBar", "name": HomeEquipment.PULLUP_BAR.value, "mapping": ["Barra"]},
                {"code": "yogaMat", "name": HomeEquipment.YOGA_MAT.value, "mapping": ["Colchoneta"]},
                {"code": "abWheel", "name": HomeEquipment.AB_WHEEL.value, "mapping": ["Rueda"]},
                {"code": "ankleWeights", "name": HomeEquipment.ANKLE_WEIGHTS.value, "mapping": ["Peso"]},
                {"code": "swissBall", "name": HomeEquipment.SWISS_BALL.value, "mapping": ["Pelota"]}
            ],
            "outdoor": [
                {"code": "track", "name": OutdoorEquipment.TRACK.value, "mapping": ["Pista"]},
                {"code": "pullupBars", "name": OutdoorEquipment.PULLUP_BARS.value, "mapping": ["Barra"]},
                {"code": "parallelBars", "name": OutdoorEquipment.PARALLEL_BARS.value, "mapping": ["Paralelas"]},
                {"code": "concreteBenches", "name": OutdoorEquipment.CONCRETE_BENCHES.value, "mapping": ["Banco"]},
                {"code": "monkeyBars", "name": OutdoorEquipment.MONKEY_BARS.value, "mapping": ["Pasamanos"]},
                {"code": "hills", "name": OutdoorEquipment.HILLS.value, "mapping": ["Cuesta"]},
                {"code": "bleachers", "name": OutdoorEquipment.BLEACHERS.value, "mapping": ["Gradas"]},
                {"code": "rings", "name": OutdoorEquipment.RINGS.value, "mapping": ["Anillas"]},
                {"code": "lowWalls", "name": OutdoorEquipment.LOW_WALLS.value, "mapping": ["Pared"]},
                {"code": "sand", "name": OutdoorEquipment.SAND.value, "mapping": ["Arena"]}
            ],
            "everyday": [
                {"code": "chair", "name": EverydayItems.CHAIR.value, "mapping": ["Silla", "Banco"]},
                {"code": "waterJugs", "name": EverydayItems.WATER_JUGS.value, "mapping": ["Garrafón", "Peso"]},
                {"code": "loadedBackpack", "name": EverydayItems.LOADED_BACKPACK.value, "mapping": ["Mochila", "Peso"]},
                {"code": "towels", "name": EverydayItems.TOWELS.value, "mapping": ["Toalla"]},
                {"code": "broomstick", "name": EverydayItems.BROOMSTICK.value, "mapping": ["Palo"]},
                {"code": "stairs", "name": EverydayItems.STAIRS.value, "mapping": ["Escalón"]},
                {"code": "sofa", "name": EverydayItems.SOFA.value, "mapping": ["Sofá"]},
                {"code": "detergentBottles", "name": EverydayItems.DETERGENT_BOTTLES.value, "mapping": ["Detergente", "Peso"]},
                {"code": "thickBooks", "name": EverydayItems.THICK_BOOKS.value, "mapping": ["Libros", "Peso"]},
                {"code": "clearWall", "name": EverydayItems.CLEAR_WALL.value, "mapping": ["Pared"]}
            ]
        }


equipment_controller = EquipmentController()
