from abc import ABC, abstractmethod
from typing import Union, Any
from datetime import datetime
from pathlib import Path
import glob, re, os

from .database import Database
from .collection import Collection
from .utilities import current_date


class Dataset(ABC):
    """
    Abstract class to define a Database query and a file path. Used to create and load a dataset.
    Provides the means to (down-)load a precomputed Collection from a server or filesystem.
    Provides methods to store to the filesystem.
    Stores files as tar bundles with sharded structures, a protein-level info file, metadata, and assets.
    Provides a Collection for the Task.
    """

    query = ""
    assets = []
    transforms = []

    def __init__(
        self,
        path: Union[str, Path] = Path(os.path.expanduser("~/.proteinshake/datasets")),
        version: str = "latest",
        download: bool = False,
    ) -> None:
        self.path = Path(path) / self.__class__.__name__
        if version == "latest":
            version = self.latest_version
        if download:
            pass
        self.load(version)

    @property
    def latest_version(self) -> str:
        files = glob.glob(f"{self.path}-v*.collection")
        versions = [re.search(r"-v(.*?)\.collection", name).group(1) for name in files]
        versions = [datetime.strptime(v, "%Y%b%d") for v in versions]
        versions.sort()
        return versions[-1] if len(versions) > 0 else None

    def version_path(self, version: str):
        return Path(f"{self.path}-v{version}.collection")

    def load(self, version: str):
        self.collection = Collection(path=self.version_path(version))

    def release(
        self,
        database: Union[str, Path] = Path("~/.proteinshake/database"),
        version: str = None,
    ) -> None:
        """
        Creates a new version of the dataset.
        """
        self.collection = Database(database).create_collection(
            query=self.query,
            assets=self.assets,
            path=self.version_path(version or current_date()),
        )
        self.collection.apply(self.transforms)
