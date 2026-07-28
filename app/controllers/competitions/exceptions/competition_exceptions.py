from app.core.exceptions import (
    NotFoundError,
    ConflictError,
    BadRequestError,
)


class CompetitionNotFoundError(NotFoundError):
    def __init__(self, message: str = "Competencia no encontrada"):
        super().__init__(message=message)


class CompetitionFullError(BadRequestError):
    def __init__(self, message: str = "La competencia ha alcanzado el máximo de participantes"):
        super().__init__(message=message)


class CompetitionCancelledError(BadRequestError):
    def __init__(self, message: str = "No puedes inscribirte en una competencia cancelada"):
        super().__init__(message=message)


class CompetitionFinishedError(BadRequestError):
    def __init__(self, message: str = "Esta competencia ya finalizó"):
        super().__init__(message=message)


class AlreadyJoinedCompetitionError(ConflictError):
    def __init__(self, message: str = "Ya estás inscrito en esta competencia"):
        super().__init__(message=message)


class ParticipantNotFoundError(NotFoundError):
    def __init__(self, message: str = "Participante no encontrado en esta competencia"):
        super().__init__(message=message)
