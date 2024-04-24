from ..dataset import Dataset
from ..adapters import LocalAdapter
from ..collection import Collection
from ..utils import current_date
from ..collection_transforms import RandomSplit
import os
from pathlib import Path


class DummyDataset(Dataset):

    def release(self, version: str = None) -> None:
        proteins = LocalAdapter(Path(os.path.expandvars("$PROTEINSHAKE_RAWDATA_PATH"))/"test_data").sync()
        self.collection = Collection(path=self.version_path(version or current_date()))
        self.collection.add_proteins(proteins)
        self.collection.add_assets(proteins.assets)
        self.collection.apply([])
