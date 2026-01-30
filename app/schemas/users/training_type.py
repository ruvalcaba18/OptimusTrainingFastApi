from enum import Enum

class TrainingType(str, Enum):
    CASA = "casa"
    AFUERA = "afuera"
    GIMNASIO = "gimnasio"
    MIXTO = "mixto"
