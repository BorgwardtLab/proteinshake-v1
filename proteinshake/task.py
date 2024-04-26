from typing import Union
import numpy as np
import os, itertools
from pathlib import Path
from functools import partial
from proteinshake.target import Target
from proteinshake.metric import Metric
from proteinshake.transform import Transform, Compose, IdentityTransform
from proteinshake.utils import sharded, save_shards, load, warn, LOCATIONS


class Task:
    dataset: str = ""
    target: Target = None
    metrics: Metric = None
    augmentation: Transform = IdentityTransform()

    def __init__(
        self,
        root: Union[str, Path] = LOCATIONS.tasks,
        shard_size: int = 1024,
    ) -> None:
        self.root = Path(root) / self.__class__.__name__
        os.makedirs(self.root, exist_ok=True)
        self.shard_size = shard_size

    def transform(self, *transforms) -> None:
        Xy = self.target(self.dataset.proteins)
        partitions = {
            split_name: filter(lambda Xy: Xy[0][0]["split"] == split_name, tee)
            for split_name, tee in zip(["train", "test", "val"], itertools.tee(Xy, 3))
        }
        self.transform = Compose(*[self.augmentation, *transforms])
        # cache from here
        self.transform.fit(partitions["train"])
        for split_name, Xy in partitions.items():
            Xy = sharded(Xy, shard_size=self.shard_size)
            data_transformed = (
                self.transform.deterministic_transform(shard) for shard in Xy
            )
            save_shards(
                data_transformed,
                self.root / split_name / hash(self.transform) / "shards",
            )
            setattr(
                self, f"{split_name}_loader", partial(self.loader, split=split_name)
            )
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
        path = self.root / split / hash(self.transform) / "shards"
        shard_index = load(path / "index.npy")
        if (
            not batch_size is None
            and self.shard_size % batch_size != 0
            and batch_size % self.shard_size != 0
        ):
            warn(
                "batch_size is not a multiple of shard_size. This causes inefficient data loading."
            )

        def generator():
            if shuffle:
                rng.shuffle(shard_index)
            shards = (load(path / f"{i}.pkl") for i in shard_index)
            for current_shard in shards:
                current_X, current_y = current_shard
                X_batch, y_batch = [], []
                while len(X_batch) < (batch_size or np.inf):
                    if batch_size is None:
                        b = len(current_X)
                    else:
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
                X_batch, y_batch = np.asarray(X_batch), np.asarray(y_batch)
                if shuffle:
                    permutation = rng.permutation(len(X_batch))
                    X_batch, y_batch = X_batch[permutation], y_batch[permutation]
                yield self.transform.stochastic_transform((X_batch, y_batch))

        return self.transform.create_loader(generator, **kwargs)

    def evaluate(self, y_true, y_pred):
        y_true = self.transform.inverse_transform(y_true)
        y_pred = self.transform.inverse_transform(y_pred)
        return self.metrics(y_true, y_pred)
