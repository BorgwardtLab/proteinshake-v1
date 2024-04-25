from ..modifier import Modifier


class SequenceLengthFilter(Modifier):

    def __init__(self, max_length=None) -> None:
        super().__init__()
