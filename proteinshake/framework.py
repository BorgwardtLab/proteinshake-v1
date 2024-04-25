from abc import ABC, abstractmethod


class Framework(ABC):
    """
    Abstract class for a framework. Used as Mixin with a Transform.
    """

    @abstractmethod
    def create_loader(self, iterator):
        """
        Creates a framework-specific dataloader from an iterator.
        """
        raise NotImplementedError
