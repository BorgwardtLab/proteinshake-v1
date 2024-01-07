class PairwiseAttributeSplitter(Splitter):
    """Compute pairwise splits based on an attribute that already exists in the dataset.
    Takes all pairs of train/val/test in the single attribute splitting setting."""

    def __init__(
        self, train_attribute: str, val_attribute: str, test_attribute: str
    ) -> None:
        self.train_attribute = train_attribute
        self.val_attribute = val_attribute
        self.test_attribute = test_attribute

    def __call__(self, dataset) -> tuple[list, list, list]:
        tmp_splitter = AttributeSplitter(
            self.train_attribute, self.val_attribute, self.test_attribute
        )
        # compute pairs of indices on the non-paired splits
        pass
