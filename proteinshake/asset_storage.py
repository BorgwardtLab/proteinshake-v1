from pathlib import Path
from typing import List


class AssetStorage:
    """
    A mapping of Asset-IDs to locations on the filesystem.
    """

    def __init__(self, path: Path) -> None:
        pass

    def get(self, assets: List[str]):
        pass
