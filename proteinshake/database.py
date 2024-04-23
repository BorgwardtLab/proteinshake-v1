from pathlib import Path
from typing import Union, List
import redis

from redis.commands.json.path import Path as RedisPath

import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query

from .collection import Collection
from .asset_storage import AssetStorage
from .structure_storage import StructureStorage
from .adapter import Adapter


class Database:
    """
    Spins up a redis database
    """

    def __init__(self, path: Path, adapters: List[Adapter] = []) -> None:
        self.assets = AssetStorage(path=path / "assets")
        self.structures = StructureStorage(path=path / "structures")
        self.adapters = adapters
        self.db = redis.Redis(host="localhost", port=6379, decode_responses=True)
        schema = (
            TextField("$.id", as_name="id"),
            TextField("$.sequence", as_name="sequence"),
        )
        self.index = self.db.ft("idx:proteins").create_index(
            schema,
            definition=IndexDefinition(prefix=["protein:"], index_type=IndexType.JSON),
        )

    def sync(self):
        for adapter in self.adapters:
            adapter.sync(self)

    def add_protein(self, protein):
        self.db.set(f"protein:{protein.id}", RedisPath.root_path(), protein.to_dict())

    def create_collection(
        self, query: str, path: Union[str, Path], assets: List[str] = []
    ):
        """
        Queries the database and returns a protein collection with metadata and assets.
        """
        proteins = self.index.search(Query(query))
        collection = Collection(path=path)
        collection.add_proteins(proteins)
        collection.add_assets(self.assets.get(assets))
        return collection
