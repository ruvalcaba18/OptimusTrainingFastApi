"""
Enterprise enums — tipos de pausa activa y duraciones válidas.
"""
from enum import Enum


class BreakDuration(int, Enum):
    """Duraciones permitidas para pausas activas (minutos)."""
    SHORT = 10
    MEDIUM = 20
    LONG = 30


class BreakCategory(str, Enum):
    """Categorías de pausas activas."""
    STRETCHING = "stretching"       # Estiramientos
    BREATHING = "breathing"         # Respiración
    MOBILITY = "mobility"           # Movilidad articular
    RELAXATION = "relaxation"       # Relajación
    EYE_CARE = "eye_care"           # Cuidado visual
    POSTURE = "posture"             # Corrección postural
