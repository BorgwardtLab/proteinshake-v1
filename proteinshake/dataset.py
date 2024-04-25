from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
import glob, os, inspect, itertools
from typing import Dict, Any, List, Union
from .modifier import Modifier
from .utils import ProteinGenerator, save, load, dict_to_avro_schema, warn
from fastavro import writer as avro_writer, reader as avro_reader

from .collection import Collection


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
        files = glob.glob(f"{self.path}-*")
        versions = [name.split("-")[-1] for name in files]
        dates = [datetime.strptime(v, "%Y%b%d") for v in versions]
        versions = [v for _, v in sorted(zip(dates, versions))]
        return versions[-1] if len(versions) > 0 else None

    def version_path(self, version: str):
        return Path(f"{self.path}-{version}")

    def load(self, version: str):
        self.collection = Collection(path=self.version_path(version))

    def add_proteins(self, proteins: List[Dict]):
        num_proteins = len(proteins)
        if not os.path.exists(self.path / "proteins.avro"):
            proteins, tee = itertools.tee(proteins)
            schema = dict_to_avro_schema(next(tee))
            os.makedirs(self.path, exist_ok=True)
            with open(self.path / "proteins.avro", "wb") as file:
                avro_writer(
                    file,
                    schema,
                    [],
                    metadata={"number_of_proteins": str(0)},
                )
        with open(self.path / "proteins.avro", "a+b") as file:
            avro_writer(
                file,
                None,
                proteins,
                metadata={"number_of_proteins": str(len(self.proteins) + num_proteins)},
            )

    def add_assets(self, assets: Dict[str, Any]) -> None:
        """
        Adds any kind of metadata to the collection.
        """
        save(assets, self.path / "assets.json")

    def apply(self, transforms: List[Modifier], replace=False):
        if not replace and inspect.stack()[1][3] == "release":
            warn(
                "self.apply() should be called with replace=True in the .release() method of a dataset."
            )
        proteins = self.proteins
        num_proteins = len(proteins)
        for transform in transforms:
            proteins = transform(proteins)
        proteins, tee = itertools.tee(proteins)
        schema = dict_to_avro_schema(next(tee))
        with open(self.path / "proteins_transformed.avro", "wb") as file:
            avro_writer(
                file,
                schema,
                proteins,
                metadata={"number_of_proteins": str(num_proteins)},
            )
        os.rename(self.path / "proteins_transformed.avro", self.path / "proteins.avro")

    @property
    def proteins(self):
        with open(self.path / "proteins.avro", "rb") as file:
            total = int(avro_reader(file).metadata["number_of_proteins"])

        assets = (
            load(self.path / "assets.json")
            if os.path.exists(self.path / "assets.json")
            else {}
        )

        def reader():
            with open(self.path / "proteins.avro", "rb") as file:
                for x in avro_reader(file):
                    yield x

        return ProteinGenerator(reader(), total, assets)

    @abstractmethod
    def release(
        self,
        version: str = None,
    ) -> None:
        """
        Creates a new version of the dataset.
        """
        raise NotImplementedError

    @abstractmethod
    def citation(self, style: str = "apa"):
        raise NotImplementedError

    @abstractmethod
    def license(self):
        raise NotImplementedError

    @abstractmethod
    def statistics(self):
        raise NotImplementedError
