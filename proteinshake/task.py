from typing import Union, List, Any, Dict
import numpy as np
import os, itertools
from pathlib import Path
from functools import partial
from proteinshake.target import Target
from proteinshake.metric import Metric
from proteinshake.transform import Transform, Compose, IdentityTransform
from proteinshake.utils import sharded, save_shards, load, warn, LOCATIONS
from numpy import ndarray


class Task:
    """A task is defined by a dataset, a target, and a set of metrics.
    It provides functionality to transform data and creates dataloaders.
    """

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

    def transform(self, *transforms: List[Transform]) -> None:
        """Applies a series of transforms to the dataset, including the target transform.
        Transformes are composed, and the deterministic part is saved to disk.
        Also realizes the split assignments and prepares the dataloaders.

        Parameters
        ----------
        transforms : List[Transform]
            A number of transforms to be applied to the dataset.
        """
        Xy = self.target(self.dataset.proteins)
        self.transform = Compose(*[self.augmentation, *transforms])
        # cache from here
        Xy, tee = itertools.tee(Xy)
        partition = filter(lambda item: item[0][0]["split"] == "train", tee)
        self.transform.fit(partition)
        for split_name in ["train", "test", "val"]:
            Xy, tee = itertools.tee(Xy)
            partition = filter(lambda item: item[0][0]["split"] == split_name, tee)
            partition = sharded(partition, shard_size=self.shard_size)
            data_transformed = (
                self.transform.deterministic_transform(shard) for shard in partition
            )
            save_shards(
                data_transformed,
                self.root / split_name / self.transform.hash() / "shards",
            )
            setattr(
                self, f"{split_name}_loader", partial(self.loader, split=split_name)
            )
        return self

    def loader(
        self,
        split: str = None,
        batch_size: int = None,
        shuffle: bool = False,
        random_seed: Union[int, None] = None,
        **kwargs,
    ) -> Any:
        """Returns a dataloader of the appropriate framework.
        Takes care of batching, efficient file loading, and application of the stochastic transforms.

        Parameters
        ----------
        split : str, optional
            The split to load, one of 'train', 'test', or 'val', by default None
        batch_size : int, optional
            The batch size, by default None
        shuffle : bool, optional
            Whether to shuffle the data, by default False
        random_seed : Union[int, None], optional
            The random seed for shuffling, by default None

        Returns
        -------
        Any
            A framework-specific dataloader.
        """
        rng = np.random.default_rng(random_seed)
        path = self.root / split / self.transform.hash() / "shards"
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

    def evaluate(self, y_true: ndarray, y_pred: ndarray) -> Dict[str, float]:
        """Computes a set of relevant metrics for the task.

        Parameters
        ----------
        y_true : ndarray
            The ground truth.
        y_pred : ndarray
            The predictions.

        Returns
        -------
        Dict[str, Float]
            A dictionary of metric names and values.
        """
        y_true = self.transform.inverse_transform(y_true)
        y_pred = self.transform.inverse_transform(y_pred)
        return self.metrics(y_true, y_pred)
