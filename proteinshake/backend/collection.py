class Collection:
    """
    Holds a set of proteins as the result of a database query and prepares it for dataset creation.
    """

    def __init__(self, proteins: list[dict]) -> None:
        pass

    def add(self, metadata: Any) -> None:
        """
        Adds any kind of metadata to the collection, such as split indices.
        """
        pass

    def save(self, name: str) -> None:
        """
        Saves the proteins and meta data in compressed format.
        """
        pass

    def upload(self, version: str = None) -> None:
        """
        Uploads the collection and meta data to Zenodo. `version` defaults to the current date.
        """
        pass
