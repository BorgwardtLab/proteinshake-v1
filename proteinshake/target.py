from typing import Dict, Iterator


class Target:
    """
    Abstract class for reshaping a dataset into the correct data-target structure for a task.
    """

    def __call__(self, dataset: Iterator[dict]) -> Dict[str, Iterator]:
        """
        Takes a dataset iterator and returns an Xy iterator, whose elements are ((X1,X2,...), y) pairs of data tuples and targets.
        """
        raise NotImplementedError
