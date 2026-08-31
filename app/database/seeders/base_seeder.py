from abc import ABC, abstractmethod
from pathlib import Path

from sqlalchemy.orm import Session


class BaseSeeder(ABC):
    def __init__(self, session: Session, data_dir: Path):
        self.session = session
        self.data_dir = data_dir

    @abstractmethod
    def seed(self) -> None:
        pass
