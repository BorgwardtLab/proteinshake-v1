class Dataset:
    def __init__(
        self,
        path: Path,
        version: str = "latest",
        shard_size: int = None,
        shuffle: bool = False,
        random_seed: int = 42,
    ) -> None:
        """
        `path` is either pointing to a Zenodo repository or a directory in the local filesystem.
        """
        pass

    def load(self):
        """
        Loads meta data.
        Returns a generator that reads and decompresses the raw files.
        """
        pass

    def save(self):
        """
        Applies the representation transforms and writes them to shards.
        """
        pass

    def apply(
        self,
        pre_representation_transform: PreRepresentationTransform = None,
        representation_transform: RepresentationTransform = None,
        post_representation_transform: PostRepresentationTransform = None,
        pre_framework_transform: PreFrameworkTransform = None,
        framework_transform: FrameworkTransform = None,
        post_framework_transform: PostFrameworkTransform = None,
    ) -> None:
        pass

    def partition(self, index):
        """
        Partitions the data according to `indices`. This will be used to retrieve subsets of the data and also to optimize sharding.
        """
        pass

    def __getitem__(self):
        """
        Intercepts representation and framework calls to forward them to `.apply()`.
        """
        pass

    def __next__(self) -> None:
        """
        Yields the next protein from a shard. When the shard is finished, loads the next one.
        If `shuffle` is True, loads a random shard and applies shuffling within the shard.
        Applies pre/framework/post transforms.
        """
        pass
