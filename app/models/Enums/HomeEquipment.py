from enum import Enum
from typing import final


@final
class HomeEquipment(str, Enum):
    RESISTANCE_BANDS = "Ligas de Resistencia con Agarres"
    MINI_BANDS = "Bandas de Glúteo (Mini-bands)"
    ADJUSTABLE_DUMBBELLS = "Mancuernas Ajustables o de Neopreno"
    JUMP_ROPE = "Cuerda para Saltar (Comba)"
    PULLUP_RACK = "Racks de Pared o Media Jaula"
    PULLUP_BAR = "Barra de Dominadas de Puerta"
    YOGA_MAT = "Tapete de Yoga / Mat"
    AB_WHEEL = "Rueda de Abdominales (Ab Wheel)"
    ANKLE_WEIGHTS = "Pesas de tobillo"
    SWISS_BALL = "Pelota de Estabilidad (Swiss Ball)"
