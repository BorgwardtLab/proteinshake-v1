from ..modifier import Modifier
from ..utils import ProteinGenerator, self_assign, error
import numpy as np


class RandomSplit(Modifier):

    def __init__(
        self,
        train_size=0.8,
        test_size=0.1,
        val_size=0.1,
    ) -> None:
        super().__init__()
        if train_size + test_size + val_size != 1:
            error("Train, test and validation split sizes do not sum to 1.")
        self.train_size = train_size
        self.test_size = test_size
        self.val_size = val_size

    def __call__(self, proteins):
        rng = np.random.default_rng(42)
        n = len(proteins)
        n_test, n_val = int(n * self.test_size), int(n * self.val_size)
        n_train = n - n_test - n_val
        index = ["train"] * n_train + ["test"] * n_test + ["val"] * n_val
        rng.shuffle(index)

        def generator():
            for protein, split in zip(proteins, index):
                protein["split"] = split
                yield protein

        return ProteinGenerator(generator(), len(proteins), proteins.assets)

    # this is just to keep the code around for multiple splits, which is currently not implemented downstream.
    def for_later(self, proteins):
        rng = np.random.default_rng(42)
        n = len(proteins)
        n_test, n_val = int(n * self.test_size), int(n * self.val_size)
        n_train = n - n_test - n_val
        splits = []
        for i in range(self.num_splits):
            index = ["train"] * n_train + ["test"] * n_test + ["val"] * n_val
            rng.shuffle(index)
            splits.append(index)
        splits = list(map(list, zip(*splits)))

        def generator():
            for protein, split in zip(proteins, split):
                protein["split"] = split
                yield protein

        return ProteinGenerator(generator(), len(proteins), proteins.assets)
