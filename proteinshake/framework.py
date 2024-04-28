from abc import ABC, abstractmethod
from typing import Tuple, Any


class Framework(ABC):
    """
    Abstract class for a framework. Used as Mixin with a Transform.
    """

    @abstractmethod
    def create_loader(self, iterator: Tuple[Tuple[Any], Any]) -> Any:
        """Creates a framework-specific dataloader from an Xy-iterator.

        Parameters
        ----------
        iterator : Tuple[Tuple[Any],Any]
            The Xy-iterator of transformed proteins.

        Returns
        -------
        Any
            The framework-specific dataloader object.
        """
        raise NotImplementedError
