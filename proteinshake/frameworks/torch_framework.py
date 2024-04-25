import torch
import numpy as np
from torch.utils.data import DataLoader, IterableDataset
from proteinshake.transform import Transform
from proteinshake.framework import Framework


class TorchFrameworkTransform(Framework, Transform):
    def transform(self, X):
        return X

    def create_loader(self, iterator, **kwargs):
        class Dataset(IterableDataset):
            def __iter__(self):
                return iterator()

        return DataLoader(Dataset(), **kwargs)