from enum import IntEnum


class ExerciseLevel(IntEnum):
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    HIGH_PERFORMANCE = 4

    @classmethod
    def from_code(cls, code: str) -> "ExerciseLevel":
        values = {
            "NIV1": cls.BASIC,
            "Básico": cls.BASIC,

            "NIV2": cls.INTERMEDIATE,
            "Intermedio": cls.INTERMEDIATE,

            "NIV3": cls.ADVANCED,
            "Avanzado": cls.ADVANCED,

            "NIV4": cls.HIGH_PERFORMANCE,
            "Alto Rendimiento": cls.HIGH_PERFORMANCE,
        }

        return values.get(code, cls.BASIC)