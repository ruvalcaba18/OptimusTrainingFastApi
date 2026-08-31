from enum import Enum
from typing import final


@final
class EverydayItems(str, Enum):
    CHAIR = "Silla Estable / Banco de Comedor"
    WATER_JUGS = "Garrafones de Agua (5L-20L)"
    LOADED_BACKPACK = "Mochila Cargada (Libros/Arroz)"
    TOWELS = "Toallas de Mano"
    BROOMSTICK = "Palo de Escoba o Fregona"
    STAIRS = "Escalones Interiores"
    SOFA = "Sofá o Sillón"
    DETERGENT_BOTTLES = "Botellas de Detergente (con asa)"
    THICK_BOOKS = "Libros Gruesos (Enciclopedias)"
    CLEAR_WALL = "Pared Despejada"
