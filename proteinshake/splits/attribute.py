class AttributeSplitter(Splitter):
    """
    Compute splits based on an attribute that already exists in the dataset
    """

    def __init__(
        self, train_attribute: str, val_attribute: str, test_attribute: str
    ) -> None:
        self.train_attribute = train_attribute
        self.val_attribute = val_attribute
        self.test_attribute = test_attribute

    def __call__(self, dataset) -> tuple[list, list, list]:
        pass
