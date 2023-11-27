from .splitter import Splitter

class TimeSplitter(Splitter):
    """ Compute splits based on an structure publication date which should be an attribute
    in the Dataset"""
    def __init__(self,
                 train_cutoff: int,
                 val_cutoff: int) -> None:

        self.train_cutoff = train_cutoff
        self.val_cutoff = val_cutoff 

    def __call__(self, dataset) -> tuple[list, list, list]:
        pass
    pass
