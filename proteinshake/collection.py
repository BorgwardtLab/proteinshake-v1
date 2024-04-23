from typing import Dict, Any, List, Union
from pathlib import Path
from .protein import Protein
from .collection_transform import CollectionTransform
from .utilities import ProteinGenerator, save, load
import os
from fastavro import writer as avro_writer, reader as avro_reader


class Collection:
    """
    A set of Proteins as a result of a Database query.
    An iterator class extending the Python class capabilities to store additional data.
    """

    def __init__(self, path: Union[str, Path]) -> None:
        self.path = Path(path)
        if not os.path.exists(self.path / "proteins.avro"):
            # write empty avro file:
            os.makedirs(self.path, exist_ok=True)
            with open(self.path / "proteins.avro", "wb") as file:
                avro_writer(
                    file,
                    Protein.avro_schema(),
                    [],
                    metadata={"number_of_proteins": str(0)},
                )

    def add_proteins(self, proteins: List[Protein]):
        with open(self.path / "proteins.avro", "a+b") as file:
            avro_writer(
                file,
                None,
                (protein.to_dict() for protein in proteins),
                metadata={
                    "number_of_proteins": str(len(self.proteins) + len(proteins))
                },
            )

    def add_assets(self, assets: Dict[str, Any]) -> None:
        """
        Adds any kind of metadata to the collection.
        """
        save(assets, self.path / "assets.json")

    def apply(self, transforms: List[CollectionTransform]):
        proteins = self.proteins
        for transform in transforms:
            proteins = transform(proteins)
        with open(self.path / "proteins_transformed.avro", "wb") as file:
            avro_writer(
                file,
                Protein.avro_schema(),
                proteins,
                metadata={"number_of_proteins": str(len(proteins))},
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
