from typing import Dict, Any, List, Union
from pathlib import Path
from .modifier import CollectionTransform
from .utils import ProteinGenerator, save, load, dict_to_avro_schema
import os, itertools
from fastavro import writer as avro_writer, reader as avro_reader


class Collection:
    """
    A set of Proteins as a result of a Database query.
    An iterator class extending the Python class capabilities to store additional data.
    """

    def __init__(self, path: Union[str, Path]) -> None:
        self.path = Path(path)

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

    def apply(self, transforms: List[CollectionTransform]):
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
