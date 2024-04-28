from typing import Iterator, Tuple, Dict, Any
from proteinshake.utils import ProteinGenerator


class Target:
    """
    Abstract class for reshaping a dataset into the correct data-target structure for a task.
    """

    def __call__(self, dataset: ProteinGenerator) -> Iterator[Tuple[Tuple[Dict], Any]]:
        """Takes a ProteinGenerator and returns an Xy-iterator whose elements are ``((X1,X2,...), y)`` pairs of data tuples and targets.

        Parameters
        ----------
        dataset : ProteinGenerator
            The dataset iterator of protein dictionaries.

        Returns
        -------
        Iterator[Tuple[Tuple[Dict], Any]]
            An Xy-iterator defining model inputs X and prediction targets y.

        """
        raise NotImplementedError
