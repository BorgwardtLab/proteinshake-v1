from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
import os, inspect, itertools
from typing import Dict, Any, List, Union
from fastavro import writer as avro_writer, reader as avro_reader
from .modifier import Modifier
from .utils import (
    ProteinGenerator,
    save,
    load,
    dict_to_avro_schema,
    warn,
    info,
    error,
    LOCATIONS,
    current_date,
)


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
        root: Union[str, Path] = LOCATIONS.datasets,
        version: str = "latest",
        online: bool = True,
    ) -> None:
        self.root = Path(root) / self.__class__.__name__
        if version == "latest":
            if online:
                version = self.latest_online_version
                if version is None:
                    info(f"{self.__class__.__name__} is not hosted. Looking locally.")
                    version = self.latest_local_version
            else:
                version = self.latest_local_version
            if version is None:
                info("Could not find dataset. Running a release.")
                version = self.release()
        if not os.path.exists(self.root / version) and (
            online and self.download(version) is None
        ):
            error(
                "Could not find {self.__class__.__name__} version {version}. Change the version or run a release by calling .release() on the dataset."
            )
        self.path = self.root / version

    @property
    def latest_local_version(self) -> str:
        versions = [entry.name for entry in os.scandir(self.root) if entry.is_dir()]
        dates = [datetime.strptime(v, "%Y%b%d") for v in versions]
        versions = [v for _, v in sorted(zip(dates, versions))]
        return versions[-1] if len(versions) > 0 else None

    @property
    def latest_online_version(self) -> str:
        return None

    def download(self, version):
        # if dataset is not hosted or version does not exist online: return None
        # download version to self.root
        return None

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
        print(inspect.stack()[1][3])
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
        version: str = current_date(),
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
