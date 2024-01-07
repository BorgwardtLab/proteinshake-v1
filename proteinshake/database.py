from pathlib import Path
from .collection import Collection


class Database:
    def __init__(self, storage: Path) -> None:
        pass

    def update(self) -> None:
        pass

    def query(self, query: str) -> Collection:
        pass
