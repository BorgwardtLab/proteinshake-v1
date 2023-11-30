import numpy as np
import random
from typing import Generic
from proteinshake.util import amino_acid_alphabet


class Dataset:
    def __init__(
        self,
        path: str = "",
        version: str = "latest",
        shard_size: int = None,
        shuffle: bool = False,
        random_seed: int = 42,
    ) -> None:
        """
        `path` is either pointing to a Zenodo repository or a directory in the local filesystem.
        """
        self.dummy_proteins = np.array(
            [
                {
                    "ID": f"protein_{i}",
                    "coords": np.random.rand(3, 300),
                    "sequence": "".join(
                        random.choice(amino_acid_alphabet) for _ in range(300)
                    ),
                    "label": np.random.random(),
                    "split": random.choice(["train", "test", "val"]),
                }
                for i in range(100)
            ]
        )

    @property
    def proteins(self):
        return iter(self.dummy_proteins)

    def apply(self, *transforms) -> Generic:
        def transform(p):
            for t in transforms:
                p = t(p)
            return p

        return (transform(p) for p in self.proteins)

    def partition(self, index: dict[np.ndarray]):
        """
        Partitions the data according to `indices`. This will be used to retrieve subsets of the data and also to optimize sharding.
        """
        self.partition = index

    def split(self, name):
        """
        Returns a new dataset with a subset of the proteins, determined by the partition.
        """
        dataset = Dataset()
        dataset.dummy_proteins = self.dummy_proteins[self.partition[name]]
        return dataset

    def create_dataloader(self, X, y):
        """
        Only temporarily a dataset class method. Will most likely be put in a dedicated `Framework` class.
        Returns a dataloader of the correct framework. For now only torch.
        """
        import torch
        from torch.utils.data import DataLoader, IterableDataset

        class _Dataset(IterableDataset):
            def __iter__(self):
                yield next(X), next(y)

        return lambda **kwargs: DataLoader(_Dataset(), **kwargs)

    def __next__(self) -> Generic:
        """
        Yields the next protein from a shard. When the shard is finished, loads the next one.
        If `shuffle` is True, loads a random shard and applies shuffling within the shard.
        Applies pre/framework/post transforms.
        """
        try:
            protein = next(self.current_shard)
        except StopIteration:
            self.current_shard = self.proteins
            protein = next(self.current_shard)
        return protein
