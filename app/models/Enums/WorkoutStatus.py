from enum import Enum
from typing import final


@final
class WorkoutStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"
