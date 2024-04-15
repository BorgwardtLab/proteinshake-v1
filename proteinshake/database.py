from pathlib import Path


class Database:
    """
    Spins up a redis database
    """

    def __init__(self, storage: Path) -> None:
        pass
    
    def adapter(self, adapter):
        """
        Adds adapter to the database.
        """
        pass

    def sync(self) -> None:
        """
        Syncs all adapters.
        """
        pass

    def query(self, query: str):
        """
        Queries the database and returns a protein collection with metadata and assets.
        """
        pass

class AssetStorage:
    """
    A mapping of Asset-IDs to locations on the filesystem.
    """

class Adapter:
    """
    Provides an API to an online database.
    """
    
    def __init__(self) -> None:
        pass
    
    def sync(self):
        pass
    

class StructureStorage:
    """
    Stores residue and atoms coordinates with meta data. Provides access by Structure-IDs.
    Structures are stored as contiguous arrays of coordinates and other residue/atom level information, in shards.
    An index file maintains the mapping from ID to shard and start/end positions.
    """
    
    def __init__(self) -> None:
        pass
    
class StructureFileProcessor:
    """
    Converts a pdb/mmcif file to a more efficient Atoms & Residue format. Implements QC.
    Applies transforms to clean and polish the structure, e.g. energy minimization.
    Also computes and annotates quality scores which can be used for later filtering.
    """
    
    def __init__(self) -> None:
        pass
    
class Protein:
    """
    A dictionary-type data structure for a protein. Contains the PS-ID, other database IDs, sequences, protein-level information, and links to assets and structures.
    """
    
    def __init__(self) -> None:
        pass
    
    
class Atoms:
    """
    A array-type data structure for the atom-level information and coordinates of a protein structure.
    """
    
    def __init__(self) -> None:
        pass
    
class Residues:
    """
    A array-type data structure for the residue-level information of a protein structure.
    """
    
    def __init__(self) -> None:
        pass
    
class Collection:
    """
    A set of Proteins as a result of a Database query. Provides methods to store to the filesystem.
    Stores files as tar bundles with sharded structures, a protein-level info file, metadata, and assets.
    """
    
    def __init__(self) -> None:
        pass
    
class ProteinIterator:
    """
    An iterator class extending the Python class capabilities to store additional data.
    """
    
    def __init__(self) -> None:
        pass
    
class CollectionTransform:
    """
    Transforms a Collection. May be used to precompute splits or filter proteins.
    Can be applied before or after write to the filesystem, i.e. can be applied before hosting or at the user-end when loading a Task.
    """
    
    def __init__(self) -> None:
        pass
    
class Dataset:
    """
    Abstract class to define a Database query and a file path. Used to create and load a dataset.
    Provides the means to (down-)load a precomputed Collection from a server or filesystem.
    Provides a ProteinIterator for the Task.
    """
    
    def __init__(self) -> None:
        pass