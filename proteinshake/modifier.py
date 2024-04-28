from proteinshake.utils import ProteinGenerator


class Modifier:
    """
    Transforms a Collection. May be used to precompute splits or filter proteins.
    """

    def __init__(self, *args, **kwargs) -> None:
        pass

    def __call__(self, proteins: ProteinGenerator) -> ProteinGenerator:
        """Modifies the protein generator.

        Parameters
        ----------
        proteins : ProteinGenerator
            An iterator of protein dictionaries.

        Returns
        -------
        ProteinGenerator
            The modified iterator.
        """
