from ..modifier import CollectionTransform


class SequenceLengthFilter(CollectionTransform):

    def __init__(self, max_length=None) -> None:
        super().__init__()
