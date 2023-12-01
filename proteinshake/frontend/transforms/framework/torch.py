import torch
from ..transform import FrameworkTransform


class TorchFrameworkTransform(FrameworkTransform):
    def transform(self, representation):
        return torch.tensor(representation)
