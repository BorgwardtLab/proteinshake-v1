class Framework:
    """
    Abstract class for a framework. Used as Mixin with a Transform.
    """

    def create_loader(self, iterator):
        """
        Creates a framework-specific dataloader from an iterator.
        """
        raise NotImplementedError
