from enum import Enum
from typing import final


@final
class OutdoorEquipment(str, Enum):
    TRACK = "Pista Atlética"
    PULLUP_BARS = "Barras Altas de Dominadas"
    PARALLEL_BARS = "Barras Paralelas de Calistenia"
    CONCRETE_BENCHES = "Bancos de Madera/Concreto"
    MONKEY_BARS = "Pasamanos / Escaleras de Mono"
    HILLS = "Cuestas de Césped o Asfalto"
    BLEACHERS = "Gradas de Estadio o Parque"
    RINGS = "Anillas de Gimnasia / Correas"
    LOW_WALLS = "Paredes de Piedra o Muros Bajos"
    SAND = "Suelo de Arena / Playa"
