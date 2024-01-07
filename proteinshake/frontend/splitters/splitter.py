class Split:
    """
    Abstract class for selecting train/val/test indices given a dataset.
    """

    @property
    def hash(self):
        return self.__class__.__name__
