import torch
from .framework import FrameworkTransform


class TorchFrameworkTransform(FrameworkTransform):
    def __call__(self, representation):
        return torch.tensor(representation)
