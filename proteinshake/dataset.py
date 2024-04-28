from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
import os, itertools
from typing import Union
from fastavro import writer as avro_writer, reader as avro_reader
from .utils import (
    ProteinGenerator,
    save,
    load,
    dict_to_avro_schema,
    info,
    error,
    LOCATIONS,
    current_date,
)


class Dataset(ABC):
    """
    Abstract class to define the dataset functionality.
    Provides means to load and store data, and access to the ProteinGenerator.
    Must implement ``release`` in any subclass.
    During testing, the ``citation``, ``license`` and ``statistics`` method will be checked.
    Implement those if you wish to merge your dataset into ProteinShake.
    """

    def __init__(
        self,
        root: Union[str, Path] = LOCATIONS.datasets,
        version: str = "latest",
        online: bool = True,
    ) -> None:
        """

        Parameters
        ----------
        root : Union[str, Path], optional
            The root directory to store data in, by default LOCATIONS.datasets
        version : str, optional
            The dataset version to load, by default "latest"
        online : bool, optional
            Whether to check the ProteinShake repository for download options, by default True
        """
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
                f"Could not find {self.__class__.__name__} version {version}. Change the version or run a release by calling .release(version_name) on the dataset."
            )
        self.path = self.root / version

    @property
    def latest_local_version(self) -> Union[str, None]:
        """Checks the local root directory for the latest available version and returns it.

        Returns
        -------
        Union[str,None]
            The name of the latest version, or None if there is no dataset.
        """
        if not os.path.exists(self.root):
            return None
        versions = [entry.name for entry in os.scandir(self.root) if entry.is_dir()]
        dates = [datetime.strptime(v, "%Y%b%d") for v in versions]
        versions = [v for _, v in sorted(zip(dates, versions))]
        return versions[-1] if len(versions) > 0 else None

    @property
    def latest_online_version(self) -> Union[str, None]:
        """Checks the ProteinShake data repository for the latest available version and returns it.

        Returns
        -------
        Union[str,None]
            The name of the latest version, or None if the dataset does not exist.
        """
        return None

    def download(self, version: str) -> Union[str, None]:
        """Downloads a version of the dataset from the ProteinShake repository.

        Parameters
        ----------
        version : str
            The version name.

        Returns
        -------
        Union[str,None]
            The name of the downloaded version, or None if the download failed.
        """
        # if dataset is not hosted or version does not exist online: return None
        # download version to self.root
        return None

    def save(
        self, proteins: ProteinGenerator, version: Union[str, None] = None
    ) -> None:
        """Saves the ProteinGenerator as version to disk.

        Parameters
        ----------
        proteins : ProteinGenerator
            The protein generator.
        version : Union[str, None], optional
            The version name, by default None
        """
        version = version or current_date()
        if os.path.exists(self.root / version):
            error(f"Version {version} alreadt exists!")
        num_proteins = len(proteins)
        self.path = self.root / version
        save(proteins.assets, self.path / "assets.json")
        proteins, tee = itertools.tee(proteins)
        schema = dict_to_avro_schema(next(tee))
        os.makedirs(self.path, exist_ok=True)
        with open(self.path / "proteins.avro", "wb") as file:
            avro_writer(
                file,
                schema,
                proteins,
                metadata={"number_of_proteins": str(num_proteins)},
            )
        return version

    @property
    def proteins(self) -> ProteinGenerator:
        """Return the ProteinGenerator of the dataset.

        Returns
        -------
        ProteinGenerator
            Iterator over protein dictionaries.
        """
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
    def release(self, version: Union[str, None] = None) -> None:
        """Creates a new version of the dataset.
        This method implements the download and processing logic.

        Parameters
        ----------
        version : Union[str, None], optional
            The version name to save the dataset under. If None, will default to the current date, by default None
        """
        raise NotImplementedError

    def citation(self, style: str = "apa") -> str:
        """Return all relevant citations of the dataset.

        Parameters
        ----------
        style : str, optional
            The citation style, by default "apa"

        Returns
        -------
        str
            The citations.
        """
        raise NotImplementedError

    def license(self) -> str:
        """Returns associated licenses for the dataset.

        Returns
        -------
        str
            The licenses.
        """
        raise NotImplementedError

    def statistics(self) -> str:
        """Computes relevant statistics of the dataset, such as label distributions.

        Returns
        -------
        str
            An html string of plots to be appended in the documentation of the dataset.
        """
        raise NotImplementedError
