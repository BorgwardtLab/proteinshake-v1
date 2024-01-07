import numpy as np
import random
from typing import Generic
from proteinshake.util import amino_acid_alphabet, save
from proteinshake.transforms import Compose
from functools import partial


class Dataset:
    def __init__(
        self,
        path: str = "",
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
                    "label": np.random.random() * 100,
                    "split": random.choice(["train", "test", "val"]),
                }
                for i in range(100)
            ]
        )

    @property
    def proteins(self):
        return iter(self.dummy_proteins)

    def split(self, splitter):
        # fitting?
        # computes splits and saves them as a dict of indices
        # rearranges protein shards for optimal data loading
        # creates ?_loader properties
        # one rng per loader
        splitter.fit(self)
        for name, index in splitter.assign(self):
            save(partition, shard_size=self.shard_size)
            setattr(self, f"{name}_index", index)
            setattr(self, f"{name}_loader", partial(self.loader, name))

    def apply(self, *transforms) -> None:
        # prepares transforms
        self.transform = Compose(transforms)
        self.transform.fit()
        for partition in self.partitions:
            save(
                self.transform.deterministic_transform(partition),
                self.root,
                shard_size=self.shard_size,
            )

    def loader(self, split=None, batch_size=None):
        # check if batch_size multiple of shard_size
        # creates generator to load data from disk (optionally shuffled) and to apply stochastic transforms
        # creates framework dataloader from self.transform.create_dataloader
        # uses the index returned from transforms to reshape the data into tuples
        def __iter__():
            # create shard order from rng
            def generator():
                try:
                    protein = next(self.current_shard)
                except StopIteration:
                    # create item order from rng
                    self.current_shard = self.proteins
                    protein = next(self.current_shard)
                return self.transform.stochastic_transform(protein)  # reshape here

            return generator

        return self.transform.create_dataloader(__iter__, batch_size=batch_size)

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
        return self.transform(protein)
