from enum import Enum


class CoachSpecialty(str, Enum):
    PERSONAL_TRAINER = "personal_trainer"
    YOGA = "yoga"
    CROSSFIT = "crossfit"
    RUNNING = "running"
    SWIMMING = "swimming"
    NUTRITION = "nutrition"
    PHYSIOTHERAPY = "physiotherapy"
    STRENGTH = "strength"
    FUNCTIONAL = "functional"
    OTHER = "other"


class BookingStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class SessionType(str, Enum):
    PRESENCIAL = "presencial"
    VIRTUAL = "virtual"
