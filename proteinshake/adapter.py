from abc import ABC, abstractmethod
from proteinshake.utils import ProteinGenerator


class Adapter(ABC):
    """
    Provides an API to an online database.
    """

    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def download(self, *args, **kwargs) -> ProteinGenerator:
        """
        Initiates the download, processes the structure files, and returns a ProteinGenerator with optional additional assets.

        Returns:
            ProteinGenerator: An iterator over protein dictionaries with optional assets.
        """
        pass
