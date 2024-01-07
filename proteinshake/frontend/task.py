from typing import Union
import numpy as np
import os
from pathlib import Path
from functools import partial
from proteinshake.frontend.splitters import Split
from proteinshake.frontend.targets import Target
from proteinshake.frontend.evaluators import Metrics
from proteinshake.frontend.transforms import Transform, Compose
from proteinshake.util import amino_acid_alphabet, sharded, save_shards, load, warn


class Task:
    dataset: str = ""
    split: Split = None
    target: Target = None
    metrics: Metrics = None
    augmentation: Transform = None

    def __init__(
        self,
        root: Union[str, None] = None,  # default path in ~/.proteinshake
        shard_size: int = 1024,
        split_kwargs: dict = {},
        target_kwargs: dict = {},
        metrics_kwargs: dict = {},
        augmentation_kwargs: dict = {},
    ) -> None:
        # create root
        if root is None:
            if not os.environ.get("PROTEINSHAKE_ROOT", None) is None:
                root = os.environ["PROTEINSHAKE_ROOT"]
            else:
                root = "~/.proteinshake"
        root = Path(root) / self.__class__.__name__
        os.makedirs(root, exist_ok=True)
        self.root = root
        self.shard_size = shard_size

        # assign task modules
        self.split = self.split(**split_kwargs)
        self.target = self.target(**target_kwargs)
        self.metrics = self.metrics(**metrics_kwargs)
        self.augmentation = self.augmentation(**augmentation_kwargs)

    @property
    def proteins(self):
        # return dataset iterator
        rng = np.random.default_rng(42)
        return (
            {
                "ID": f"protein_{i}",
                "coords": rng.integers(0, 100, size=(300, 3)),
                "sequence": "".join(
                    rng.choice(list(amino_acid_alphabet)) for _ in range(300)
                ),
                "label": rng.random() * 100,
                "split": rng.choice(["train", "test", "val"]),
            }
            for i in range(100)
        )

    def transform(self, *transforms) -> None:
        Xy = self.target(self.proteins)
        partitions = self.split(Xy)  # returns dict of generators[(X,...),y]
        self.transform = Compose(*[self.augmentation, *transforms])
        # cache from here
        self.transform.fit(partitions["train"])
        for name, Xy in partitions.items():
            Xy = sharded(Xy, shard_size=self.shard_size)
            data_transformed = (
                self.transform.deterministic_transform(shard) for shard in Xy
            )
            save_shards(
                data_transformed,
                self.root / self.split.hash / self.transform.hash / "shards",
            )
            setattr(self, f"{name}_loader", partial(self.loader, split=name))
        return self

    def loader(
        self,
        split=None,
        batch_size=None,
        shuffle: bool = False,
        random_seed: Union[int, None] = None,
        **kwargs,
    ):
        rng = np.random.default_rng(random_seed)
        path = self.root / self.split.hash / self.transform.hash / "shards"
        shard_index = load(path / "index.npy")
        if self.shard_size % batch_size != 0 and batch_size % self.shard_size != 0:
            warn(
                "batch_size is not a multiple of shard_size. This causes inefficient data loading."
            )

        def generator():
            if shuffle:
                rng.shuffle(shard_index)
            shards = (load(path / f"{i}.pkl") for i in shard_index)
            while current_shard := next(shards):
                current_X, current_y = current_shard
                X_batch, y_batch = [], []
                while len(X_batch) < batch_size:
                    b = batch_size - len(X_batch)
                    X_piece, current_X = current_X[:b], current_X[b:]
                    y_piece, current_y = current_y[:b], current_y[b:]
                    X_batch = X_batch + list(X_piece)
                    y_batch = y_batch + list(y_piece)
                    if len(current_X) == 0:
                        try:
                            current_shard = next(shards)
                            current_X, current_y = current_shard
                        except StopIteration:
                            break
                yield self.transform.stochastic_transform(
                    (np.asarray(X_batch), np.asarray(y_batch))
                )

        return self.transform.create_loader(generator, **kwargs)

    def evaluate(self, y_true, y_pred):
        y_true = self.transform.inverse_transform(y_true)
        y_pred = self.transform.inverse_transform(y_pred)
        return self.metrics(y_true, y_pred)
