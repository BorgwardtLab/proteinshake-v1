class Dataset:
    def __init__(
        self,
        path: Path,
        version: str = "latest",
        shard_size: int = None,
        batch_size: int = None,
        shuffle: bool = False,
        random_seed: int = 42,
    ) -> None:
        """
        Takes a compressed collection and applies transforms.
        `path` is either pointing to a Zenodo repository or a directory in the local filesystem.
        """
        pass

    def to_graph(
        self,
        pre_transform: PreRepresentationTransform = None,
        post_transform: PostRepresentationTransform = None,
        **kwargs
    ) -> Dataset:
        """
        Applies pre/representation/post transforms to all proteins in the dataset.
        """
        self.proteins.apply(pre_transform)
        self.proteins.apply(GraphTransform(**kwargs))
        self.proteins.apply(post_transform)
        return self

    def pyg(
        self,
        pre_transform: PreFrameworkTransform = None,
        post_transform: PostFrameworkTransform = None,
        **kwargs
    ) -> Generic:
        """
        Creates an iterable that wraps around __next__ or __getitem__ and applies pre/framework/post transforms.
        Returns a framework-specific dataset instance (iterable-style if sharded, map-style if in-memory or on-disk).
        """
        pass

    def __next__(self) -> None:
        """
        Yields the next protein from a shard. When the shard is finished, loads the next one.
        If `shuffle` is True, loads a random shard and applies shuffling within the shard.
        """
        pass

    def __getitem__(self, index: Union[int, list, tuple, ndarray]) -> None:
        """
        Returns the indexed proteins. Not available with sharding for performance reasons.
        """
        pass
