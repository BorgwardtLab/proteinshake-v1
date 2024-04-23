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

    def __init__(
        self,
        path: Union[str, Path] = Path.home() / ".proteinshake" / "datasets",
        version: str = "latest",
        download: bool = False,
    ) -> None:
        self.path = Path(path) / self.__class__.__name__
        if version == "latest":
            version = self.latest_version
        if download:
            pass
        if os.path.exists(self.version_path(version)):
            self.load(version)
        else:
            self.release()

    @property
    def latest_version(self) -> str:
        files = glob.glob(f"{self.path}-*.collection")
        versions = [re.search(r"-(.*?)\.collection", name).group(1) for name in files]
        dates = [datetime.strptime(v, "%Y%b%d") for v in versions]
        versions = [v for _, v in sorted(zip(dates, versions))]
        return versions[-1] if len(versions) > 0 else None

    def version_path(self, version: str):
        return Path(f"{self.path}-{version}.collection")

    def load(self, version: str):
        self.collection = Collection(path=self.version_path(version))

    @abstractmethod
    def release(
        self,
        version: str = None,
    ) -> None:
        """
        Creates a new version of the dataset.
        """
        return
