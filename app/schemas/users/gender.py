from enum import Enum

class UserGender(str, Enum):
    MALE = "hombre"
    FEMALE = "mujer"
    OTHER = "otro"
