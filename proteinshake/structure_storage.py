from pathlib import Path


class StructureStorage:
    """
    Stores residue and atoms coordinates with meta data. Provides access by Structure-IDs.
    Structures are stored as contiguous arrays of coordinates and other residue/atom level information, in shards.
    An index file maintains the mapping from ID to shard and start/end positions.
    """

    def __init__(self, path: Path) -> None:
        pass
