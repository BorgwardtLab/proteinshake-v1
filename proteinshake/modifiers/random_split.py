from ..modifier import Modifier
from ..utils import ProteinGenerator, self_assign, error
import numpy as np


class RandomSplit(Modifier):

    @self_assign
    def __init__(
        self,
        num_splits=5,
        train_size=0.8,
        test_size=0.1,
        val_size=0.1,
    ) -> None:
        super().__init__()
        if train_size + test_size + val_size != 1:
            error("Train, test and validation split sizes do not sum to 1.")

    def __call__(self, proteins):
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
