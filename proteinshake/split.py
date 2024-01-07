from typing import Dict, Iterator


class Split:
    """
    Abstract class to create data splits from a dataset.
    """

    def __call__(self, dataset: Iterator) -> Dict[str, Iterator]:
        """
        Takes an Xy iterator and returns a dictionary of Xy iterators, where each key denotes the split name (usually 'train', 'test', and 'val').
        """
        raise NotImplementedError

    @property
    def hash(self):
        return self.__class__.__name__
