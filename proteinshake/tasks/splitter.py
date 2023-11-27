class Splitter:
""" Abstract class for selecting train/val/test indices given a dataset.
"""
    def __call__(self, dataset) -> tuple[list, list, list]:
        raise NotImplementedError
