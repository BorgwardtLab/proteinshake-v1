from pathlib import Path
from typing import Union, List

from .collection import Collection
from .asset_storage import AssetStorage
from .structure_storage import StructureStorage


class Database:
    """
    Spins up a redis database
    """

    def __init__(self, storage: Path) -> None:
        self.assets = AssetStorage(path=storage / "assets")
        self.structures = StructureStorage(path=storage / "structures")

    def create_collection(
        self, query: str, path: Union[str, Path], assets: List[str] = []
    ):
        """
        Queries the database and returns a protein collection with metadata and assets.
        """
        import numpy as np
        from .utilities import amino_acid_alphabet

        rng = np.random.default_rng(42)
        dummies = [
            {
                "ID": f"protein_{i}",
                "x": rng.integers(0, 100, size=300),
                "y": rng.integers(0, 100, size=300),
                "z": rng.integers(0, 100, size=300),
                "sequence": "".join(
                    rng.choice(list(amino_acid_alphabet)) for _ in range(300)
                ),
            }
            for i in range(100)
        ]

        collection = Collection(path=path)
        collection.add_proteins(dummies)
        collection.add_assets(self.assets.get(assets))
        return collection
