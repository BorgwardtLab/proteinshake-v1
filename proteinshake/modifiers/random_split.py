from ..modifier import Modifier
from ..utils import ProteinGenerator
from sklearn.model_selection import train_test_split
import numpy as np


class RandomSplit(Modifier):

    def __init__(self, num_splits=5) -> None:
        super().__init__()
        self.num_splits = num_splits

    def __call__(self, proteins):
        index = np.arange(len(proteins))
        train, testval = train_test_split(index, test_size=0.2, random_state=0)
        test, val = train_test_split(testval, test_size=0.5, random_state=0)

        def generator():
            for protein in proteins:
                yield protein

        return ProteinGenerator(generator(), len(proteins), proteins.assets)
