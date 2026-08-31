from enum import Enum
from typing import final


@final
class GymEquipment(str, Enum):
    DUMBBELLS = "Mancuernas de Peso Libre"
    MACHINES = "Máquinas de Palanca/Placas"
    CABLES = "Sistemas de Poleas Ajustables"
    RACKS = "Racks, Jaulas y Smith"
    BARBELL = "Barras Olímpicas y Discos"
    PLYO_BOX = "Cajones Pliométricos"
    HEAVY_BAG = "Costales de Boxeo / MMA"
    ASSAULT_BIKE = "Bicicletas de Resistencia"
    BENCHES = "Bancos de Musculación"
    KETTLEBELLS = "Kettlebells (Pesas Rusas)"
